要查看Chrome浏览器中的扩展是否获取了剪切板的权限，你可以通过以下步骤进行检查：

### 步骤一：打开扩展管理页面

1. 打开Chrome浏览器。
2. 点击右上角的三点菜单（更多操作）。
3. 选择“更多工具（More tools）”。
4. 点击“扩展程序（Extensions）”。你也可以直接在地址栏输入 `chrome://extensions/` 然后按回车键。

### 步骤二：查看扩展的详细信息

在扩展管理页面，你会看到所有已安装的扩展程序。找到你感兴趣的扩展，然后点击“详细信息（Details）”。

### 步骤三：检查扩展的权限

在扩展的详细信息页面，你可以查看该扩展所请求的权限。注意，这里展示的是扩展在`manifest.json`文件中声明的权限，并不一定会明确指出具体的剪切板权限。不过，如果扩展声明了以下权限，它可能有能力访问剪切板：

- `clipboardRead`：允许扩展读取剪切板内容。
- `clipboardWrite`：允许扩展写入剪切板内容。

### 示例：

```json
{
  "name": "Example Extension",
  "version": "1.0",
  "manifest_version": 2,
  "permissions": [
    "clipboardRead",
    "clipboardWrite"
  ],
  "background": {
    "scripts": ["background.js"],
    "persistent": false
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"]
    }
  ],
  "browser_action": {
    "default_popup": "popup.html"
  }
}
```

上述示例中的扩展声明了`clipboardRead`和`clipboardWrite`权限，这意味着它可以读取和写入剪切板内容。

### 手动检查剪切板操作

如果你怀疑某个扩展在未经授权的情况下访问了剪切板，你可以通过以下方法手动检查：

1. **禁用可疑扩展**：在扩展管理页面禁用或删除可疑的扩展。
2. **监视剪切板操作**：手动监视剪切板内容的变化，确保没有意外的数据被写入或读取。

### 使用开发者工具查看剪贴板访问

如果你具备一定的技术能力，可以使用Chrome开发者工具来监视剪贴板操作：

1. 打开开发者工具（按 `Ctrl+Shift+I` 或 `F12`）。
2. 切换到“Console”标签页。
3. 输入以下命令来监视剪贴板读取操作：

```javascript
document.addEventListener('paste', function(event) {
    console.log('Pasted content:', event.clipboardData.getData('Text'));
});
```

### 总结

通过上述方法，你可以检查Chrome扩展是否具备剪切板访问权限。始终保持警惕并定期检查已安装的扩展程序，以确保系统的安全和隐私。如果发现可疑行为，及时禁用或删除相关扩展，并考虑使用安全软件进行进一步的检测和保护。