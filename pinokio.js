const path = require("path")
module.exports = {
  version: "3.0",
  title: "XTTS",
  description: "clone voices into different languages by using just a quick 3-second audio clip. (a local version of https://huggingface.co/spaces/coqui/xtts)",
  icon: "icon.png",
  menu: async (kernel, info) => {
    let installed = info.exists("env")
    let running = {
      install: info.running("install.json"),
      start: info.running("start.json"),
      update: info.running("update.js"),
      reset: info.running("reset.js")
    }
    if (running.install) {
      return [{
        default: true,
        icon: "fa-solid fa-plug",
        text: "Installing",
        href: "install.json",
      }]
    } else if (running.update) {
      return [{
        default: true,
        icon: 'fa-solid fa-terminal',
        text: "Updating",
        href: "update.js",
      }]
    } else if (installed) {
      if (running.start) {
        let local = info.local("start.json")
        if (local && local.url) {
          return [{
            default: true,
            icon: "fa-solid fa-rocket",
            text: "Open Web UI",
            href: local.url,
          }, {
            icon: 'fa-solid fa-terminal',
            text: "Terminal",
            href: "start.json",
          }]
        } else {
          return [{
            default: true,
            icon: 'fa-solid fa-terminal',
            text: "Terminal",
            href: "start.json",
          }]
        }
      } else if (running.reset) {
          return [{
            default: true,
            icon: 'fa-solid fa-terminal',
            text: "Resetting",
            href: "reset.js",
          }]
      } else {
        return [{
          default: true,
          icon: "fa-solid fa-power-off",
          text: "Start",
          href: "start.json",
        }, {
          icon: "fa-solid fa-plug",
          text: "Update",
          href: "update.js",
        }, {
          icon: "fa-solid fa-plug",
          text: "Install",
          href: "install.json",
        }, {
          icon: "fa-regular fa-circle-xmark",
          text: "Reset",
          href: "reset.js",
        }]
      }
    } else {
      return [{
        default: true,
        icon: "fa-solid fa-plug",
        text: "Install",
        href: "install.json",
      }]
    }
  }
}
