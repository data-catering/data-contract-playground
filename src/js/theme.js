import { getCurrentAceTheme } from "./util.js"

export function applyInitialTheme() {
  const saved = localStorage.getItem("theme")
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
  const initial = saved || (prefersDark ? "dark" : "light")
  document.documentElement.dataset.theme = initial
}

export function initThemeToggle(buttonId, editors = []) {
  const button = document.getElementById(buttonId)
  if (!button) return
  button.addEventListener("click", () => {
    const root = document.documentElement
    const next = (root.dataset.theme || "light") === "light" ? "dark" : "light"
    root.dataset.theme = next
    localStorage.setItem("theme", next)
    editors.forEach(ed => {
      try { ed.setTheme(getCurrentAceTheme()) } catch (e) {}
    })
  })
}



