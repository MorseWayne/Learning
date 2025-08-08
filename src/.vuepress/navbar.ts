import { navbar } from "vuepress-theme-hope";

export default navbar([
  "/",
   {
    text: "编程语言",
    prefix: "/docs/language/",
    icon: "solar:programming-bold",
    children: [
      "cpp/"
    ],
  },
  {
    text: "数据库",
    prefix: "/docs/database/",
    icon: "ant-design:database-filled",
    children: [
      "redis/"
    ],
  },
  "/docs/algorithm/",
  {
    text: "Web Server",
    prefix: "/docs/web_server/",
    icon: "mdi:server-network",
    children: [
      "nginx/"
    ],
  },
  "/docs/interview/",
]);
