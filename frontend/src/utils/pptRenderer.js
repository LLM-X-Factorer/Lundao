import { marked } from 'marked'
import markedKatex from 'marked-katex-extension'
import hljs from 'highlight.js/lib/core'
import DOMPurify from 'dompurify'

// 按需导入常用语言（避免全量导入）
import javascript from 'highlight.js/lib/languages/javascript'
import python from 'highlight.js/lib/languages/python'
import java from 'highlight.js/lib/languages/java'
import cpp from 'highlight.js/lib/languages/cpp'
import sql from 'highlight.js/lib/languages/sql'
import bash from 'highlight.js/lib/languages/bash'
import json from 'highlight.js/lib/languages/json'

// 注册语言
hljs.registerLanguage('javascript', javascript)
hljs.registerLanguage('python', python)
hljs.registerLanguage('java', java)
hljs.registerLanguage('cpp', cpp)
hljs.registerLanguage('sql', sql)
hljs.registerLanguage('bash', bash)
hljs.registerLanguage('json', json)

/**
 * 配置marked扩展
 */
// 1. KaTeX数学公式支持
marked.use(markedKatex({
  throwOnError: false,     // 公式错误时不中断渲染
  output: 'html',          // 输出HTML格式
  displayMode: false,      // 行内公式模式
  strict: false            // 宽松解析
}))

// 2. 代码高亮支持
marked.setOptions({
  gfm: true,               // GitHub Flavored Markdown
  breaks: true,            // 换行符转<br>
  headerIds: false,        // 禁用标题ID（幻灯片不需要锚点）
  highlight: (code, lang) => {
    // 如果指定了语言且支持，则高亮
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(code, { language: lang }).value
      } catch (err) {
        console.warn('Highlight.js error:', err)
      }
    }
    // 否则返回原始代码（自动转义）
    return code
  }
})

/**
 * 将Markdown拆分为幻灯片数组
 * @param {string} markdown - 完整的Markdown文本
 * @returns {string[]} 幻灯片数组
 */
export function parseSlides(markdown) {
  if (!markdown || typeof markdown !== 'string') {
    return []
  }

  return markdown
    .split(/^---$/m)  // 使用 --- 作为分隔符（独立行）
    .map(slide => slide.trim())
    .filter(slide => slide.length > 0)
}

/**
 * 渲染单个幻灯片的Markdown为HTML
 * @param {string} slideMarkdown - 单页幻灯片的Markdown
 * @returns {string} 清理后的HTML
 */
export function renderSlide(slideMarkdown) {
  if (!slideMarkdown || typeof slideMarkdown !== 'string') {
    return '<p class="text-gray-400">空白页</p>'
  }

  try {
    // Step 1: Markdown → HTML (包含KaTeX和代码高亮)
    const rawHtml = marked.parse(slideMarkdown)

    // Step 2: 安全清理（防止XSS）
    const sanitizedHtml = DOMPurify.sanitize(rawHtml, {
      ALLOWED_TAGS: [
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'p', 'br', 'strong', 'em', 'u', 's', 'code', 'pre', 'span',
        'ul', 'ol', 'li',
        'table', 'thead', 'tbody', 'tr', 'th', 'td',
        'blockquote', 'a', 'img',
        // KaTeX需要的标签
        'annotation', 'math', 'mrow', 'mi', 'mo', 'mn', 'mtext', 'mspace',
        'semantics', 'mstyle', 'msup', 'msub', 'mfrac', 'mover', 'munder'
      ],
      ALLOWED_ATTR: [
        'href', 'src', 'alt', 'title', 'class', 'style',
        // KaTeX需要的属性
        'xmlns', 'encoding', 'data-*'
      ],
      // 允许KaTeX的style属性
      ALLOWED_STYLES: {
        '*': {
          'color': [/^#[0-9a-f]{3,6}$/i],
          'font-size': [/^\d+(?:\.\d+)?(?:px|em|rem|%)$/],
          'margin': [/^\d+(?:\.\d+)?(?:px|em|rem)$/],
          'padding': [/^\d+(?:\.\d+)?(?:px|em|rem)$/]
        }
      }
    })

    return sanitizedHtml
  } catch (error) {
    console.error('Slide rendering error:', error)
    return `<p class="text-red-500">渲染错误: ${error.message}</p>`
  }
}

/**
 * 渲染所有幻灯片
 * @param {string} markdown - 完整的Markdown文本
 * @returns {string[]} 渲染后的HTML数组
 */
export function renderAllSlides(markdown) {
  const slides = parseSlides(markdown)
  return slides.map(slide => renderSlide(slide))
}
