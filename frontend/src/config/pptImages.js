/**
 * PPT图片路径配置
 * 管理每篇论文的PPT截图路径和数量
 */

/**
 * 图片基础路径
 */
const BASE_IMAGE_PATH = '/ppt-images'

/**
 * 论文ID到图片目录的映射
 * 每个论文对应一个目录，目录内包含slide-{n}.png格式的截图
 */
export const PAPER_IMAGE_DIRS = {
  'daily-0001': `${BASE_IMAGE_PATH}/daily-0001`,
  'daily-0002': `${BASE_IMAGE_PATH}/daily-0002`,
  'daily-0003': `${BASE_IMAGE_PATH}/daily-0003`,
  'daily-0004': `${BASE_IMAGE_PATH}/daily-0004`,
  'daily-0005': `${BASE_IMAGE_PATH}/daily-0005`,
  'daily-0006': `${BASE_IMAGE_PATH}/daily-0006`,
  'daily-0007': `${BASE_IMAGE_PATH}/daily-0007`,
  'daily-0008': `${BASE_IMAGE_PATH}/daily-0008`
}

/**
 * 默认的幻灯片数量（当无法动态检测时使用）
 * 实际使用时会尝试动态检测，这只是fallback值
 */
export const DEFAULT_SLIDE_COUNTS = {
  'daily-0001': 10,  // 默认10张，实际会根据上传的图片数量更新
  'daily-0002': 10,
  'daily-0003': 10,
  'daily-0004': 10,
  'daily-0005': 10,
  'daily-0006': 10,
  'daily-0007': 10,
  'daily-0008': 10
}

/**
 * 支持的图片格式
 */
export const IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg']

/**
 * 根据paperId和slide索引生成图片URL
 * @param {string} paperId - 论文ID
 * @param {number} slideIndex - 幻灯片索引（从1开始）
 * @param {string} extension - 图片扩展名（默认.png）
 * @returns {string} 图片URL
 */
export function getSlideImageUrl(paperId, slideIndex, extension = '.png') {
  const dir = PAPER_IMAGE_DIRS[paperId]
  if (!dir) {
    console.warn(`[PPT Images] Unknown paperId: ${paperId}`)
    return ''
  }
  return `${dir}/slide-${slideIndex}${extension}`
}

/**
 * 获取论文的所有幻灯片图片URL数组
 * @param {string} paperId - 论文ID
 * @param {number} slideCount - 幻灯片总数
 * @param {string} extension - 图片扩展名（默认.png）
 * @returns {Array<{index: number, url: string}>} 图片URL数组
 */
export function getAllSlideUrls(paperId, slideCount, extension = '.png') {
  const slides = []
  for (let i = 1; i <= slideCount; i++) {
    slides.push({
      index: i,
      url: getSlideImageUrl(paperId, i, extension)
    })
  }
  return slides
}

/**
 * 检测论文的实际幻灯片数量（通过尝试加载图片）
 * 注意：这是一个异步操作，会尝试加载图片来确定数量
 * @param {string} paperId - 论文ID
 * @param {number} maxSlides - 最大检测数量（默认50）
 * @returns {Promise<number>} 实际幻灯片数量
 */
export async function detectSlideCount(paperId, maxSlides = 50) {
  const dir = PAPER_IMAGE_DIRS[paperId]
  if (!dir) {
    return 0
  }

  // 二分查找最大索引
  // let left = 1
  // let right = maxSlides
  let maxFound = 0

  const checkImageExists = async (index) => {
    for (const ext of IMAGE_EXTENSIONS) {
      const url = getSlideImageUrl(paperId, index, ext)
      try {
        const response = await fetch(url, { method: 'HEAD' })
        if (response.ok) {
          return true
        }
      } catch {
        // 忽略错误，继续尝试下一个扩展名
      }
    }
    return false
  }

  // 先检查第一张图片是否存在
  const firstExists = await checkImageExists(1)
  if (!firstExists) {
    return DEFAULT_SLIDE_COUNTS[paperId] || 0
  }

  // 线性扫描找到最后一张
  for (let i = 1; i <= maxSlides; i++) {
    const exists = await checkImageExists(i)
    if (exists) {
      maxFound = i
    } else {
      // 连续3张不存在就停止
      const next1 = await checkImageExists(i + 1)
      const next2 = await checkImageExists(i + 2)
      if (!next1 && !next2) {
        break
      }
    }
  }

  return maxFound
}

/**
 * 批量检测所有论文的幻灯片数量
 * @returns {Promise<Object>} paperId -> slideCount映射
 */
export async function detectAllSlideCounts() {
  const counts = {}
  const paperIds = Object.keys(PAPER_IMAGE_DIRS)

  for (const paperId of paperIds) {
    try {
      counts[paperId] = await detectSlideCount(paperId)
    } catch (error) {
      console.error(`[PPT Images] Failed to detect slide count for ${paperId}:`, error)
      counts[paperId] = DEFAULT_SLIDE_COUNTS[paperId] || 0
    }
  }

  return counts
}

/**
 * 预加载指定论文的所有幻灯片图片
 * @param {string} paperId - 论文ID
 * @param {number} slideCount - 幻灯片总数
 * @returns {Promise<void>}
 */
export async function preloadSlideImages(paperId, slideCount) {
  const slides = getAllSlideUrls(paperId, slideCount)
  const promises = slides.map(slide => {
    return new Promise((resolve) => {
      const img = new Image()
      img.onload = resolve
      img.onerror = resolve  // 即使失败也继续
      img.src = slide.url
    })
  })

  await Promise.all(promises)
}
