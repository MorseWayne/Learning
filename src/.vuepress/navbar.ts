import { navbar } from "vuepress-theme-hope";

export default navbar([
  "/",
   {
    text: "编程语言",
    prefix: "/docs/language/",
    icon: "/assets/icons/programming.svg",
    children: [
      "cpp/"
    ],
  },
  {
    text: "数据库",
    prefix: "/docs/database/",
    icon: "/assets/icons/database.svg",
    children: [
      "redis/"
    ],
  },
  "/docs/algorithm/",
  {
    text: "Web Server",
    prefix: "/docs/web_server/",
    icon: "/assets/icons/server.svg",
    children: [
      "nginx/"
    ],
  },
  "/docs/interview/",
]);
