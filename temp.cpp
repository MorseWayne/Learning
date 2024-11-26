diff --git a/window_scene/session/host/include/session.h b/window_scene/session/host/include/session.h
index fa3eb0826..85ca3f5bd 100644
--- a/window_scene/session/host/include/session.h
+++ b/window_scene/session/host/include/session.h
@@ -547,6 +547,11 @@ public:
     std::optional<bool> GetClientDragEnable() const;
     std::shared_ptr<AppExecFwk::EventHandler> GetEventHandler() const;
 
+    /**
+     * Lock Screen
+     */
+    bool IsBelongToLockScreenWindow() const;
+
 protected:
     class SessionLifeCycleTask : public virtual RefBase {
     public:
@@ -844,6 +849,11 @@ private:
      * Window Layout
      */
     std::optional<bool> clientDragEnable_;
+
+    /**
+     * Lock Screen
+     */
+    std::atomic_bool isBelongToLockScreenWindow_ { false};
 };
 } // namespace OHOS::Rosen
 
diff --git a/window_scene/session/host/src/scene_session.cpp b/window_scene/session/host/src/scene_session.cpp
index ad7ddebb7..aea4338e8 100644
--- a/window_scene/session/host/src/scene_session.cpp
+++ b/window_scene/session/host/src/scene_session.cpp
@@ -214,11 +214,6 @@ bool SceneSession::IsShowOnLockScreen(uint32_t lockScreenZOrder)
         return false;
     }
 
-    if (!GetStateFromManager(ManagerState::MANAGER_STATE_SCREEN_LOCKED)) {
-        TLOGD(WmsLogTag::WMS_UIEXT, "UIExtOnLock: not in lock screen");
-        return false;
-    }
-
     // current window on lock screen jurded by zorder
     if (zOrder_ >= lockScreenZOrder) {
         TLOGI(WmsLogTag::WMS_UIEXT, "UIExtOnLock: zOrder_ is no more than lockScreenZOrder");
diff --git a/window_scene/session/host/src/session.cpp b/window_scene/session/host/src/session.cpp
index abd68339a..399c3a4e3 100755
--- a/window_scene/session/host/src/session.cpp
+++ b/window_scene/session/host/src/session.cpp
@@ -15,6 +15,8 @@
 
 #include "session/host/include/session.h"
 
+#include <regex>
+
 #include "ability_info.h"
 #include "input_manager.h"
 #include "key_event.h"
@@ -96,6 +98,12 @@ Session::Session(const SessionInfo& info) : sessionInfo_(info)
         TLOGI(WmsLogTag::WMS_FOCUS, "focusedOnShow:%{public}d", focusedOnShow);
         SetFocusedOnShow(focusedOnShow);
     }
+
+    static const std::regex pattern(R"(^SCBScreenLock[0-9]+$)");
+    if (std::regex_match(info.bundleName_, pattern)) {
+        TLOGD(WmsLogTag::DEFAULT, "bundleName: %{public}s", info.bundleName_.c_str());
+        isBelongToLockScreenWindow_ = true;
+    }
 }
 
 Session::~Session()
@@ -1407,6 +1415,11 @@ std::optional<bool> Session::GetClientDragEnable() const
     return clientDragEnable_;
 }
 
+bool Session::IsBelongToLockScreenWindow() const
+{
+    return isBelongToLockScreenWindow_.load();
+}
+
 void Session::NotifyForegroundInteractiveStatus(bool interactive)
 {
     SetForegroundInteractiveStatus(interactive);
diff --git a/window_scene/session_manager/src/scene_session_manager.cpp b/window_scene/session_manager/src/scene_session_manager.cpp
index 30a1259e6..9946b3b29 100755
--- a/window_scene/session_manager/src/scene_session_manager.cpp
+++ b/window_scene/session_manager/src/scene_session_manager.cpp
@@ -1506,16 +1506,9 @@ WMError SceneSessionManager::CheckWindowId(int32_t windowId, int32_t& pid)
 uint32_t SceneSessionManager::GetLockScreenZorder()
 {
     std::shared_lock<std::shared_mutex> lock(sceneSessionMapMutex_);
-    for (const auto& [persistentId, session] : sceneSessionMap_) {
-        if (session && (session->GetWindowType() == WindowType::WINDOW_TYPE_KEYGUARD)) {
-            static const std::regex pattern(R"(^SCBScreenLock[0-9]+$)");
-            auto& bundleName = session->GetSessionInfo().bundleName_;
-            if (!std::regex_match(bundleName, pattern)) {
-                TLOGD(WmsLogTag::WMS_UIEXT, " bundleName: %{public}s", bundleName.c_str());
-                continue;
-            }
-            TLOGI(WmsLogTag::WMS_UIEXT, "UIExtOnLock: found window %{public}d, bundleName: %{public}s", persistentId,
-                bundleName.c_str());
+    for (auto& [persistentId, session] : sceneSessionMap_) {
+        if (session && session->IsBelongToLockScreenWindow()) {
+            TLOGI(WmsLogTag::WMS_UIEXT, "UIExtOnLock: found window %{public}d", persistentId);
             return session->GetZOrder();
         }
     }
@@ -1535,6 +1528,11 @@ WMError SceneSessionManager::CheckUIExtensionCreation(int32_t windowId, uint32_t
         }
         pid = sceneSession->GetCallingPid();
 
+        if (!sceneSession->GetStateFromManager(ManagerState::MANAGER_STATE_SCREEN_LOCKED)) {
+            TLOGND(WmsLogTag::WMS_UIEXT, "UIExtOnLock: not in lock screen");
+            return WMError::WM_OK;
+        }
+
         // 1. check window whether can show on main window
         if (!sceneSession->IsShowOnLockScreen(GetLockScreenZorder())) {
             TLOGNI(WmsLogTag::WMS_UIEXT, "UIExtOnLock: not called on lock screen");
