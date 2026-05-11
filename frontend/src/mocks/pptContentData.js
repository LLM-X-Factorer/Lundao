/**
 * Mock PPT Content Data - Image-Based Preview
 * PPT内容以图片形式展示，每篇论文对应一系列截图
 */

/**
 * PPT内容数据库（taskId → content映射）
 * 新结构：每个任务包含图片URL数组，而非Markdown
 */
export const mockPPTContents = {
  // 论文1: WM-MoE (Autonomous Driving Corner Cases)
  'daily-0001': {
    taskId: 'daily-0001',
    paperId: 'daily-0001',
    type: 'images',
    slides: [],  // 图片URL数组，将在运行时动态填充
    totalSlides: 14,  // 总幻灯片数（实际图片数量）
    metadata: {
      paperTitle: 'Addressing Corner Cases in Autonomous Driving: A World Model-based Approach with Mixture of Experts and LLMs',
      generatedAt: '2024-10-29T10:00:00.000Z',
      author: 'Haicheng Liao, Bonan Wang, Junxian Yang, et al.',
      field: 'Computer Vision'
    }
  },

  // 论文2: Grey Wolf Optimizer for Federated Learning
  'daily-0002': {
    taskId: 'daily-0002',
    paperId: 'daily-0002',
    type: 'images',
    slides: [],
    totalSlides: 19,  // 实际图片数量
    metadata: {
      paperTitle: 'A Green Multi-Attribute Client Selection for Over-The-Air Federated Learning: A Grey-Wolf-Optimizer Approach',
      generatedAt: '2024-09-17T10:05:00.000Z',
      author: 'Maryam Ben Driss, Essaid Sabir, Halima Elbiaze, et al.',
      field: 'Machine Learning'
    }
  },

  // 论文3: Meta-Chunking for RAG
  'daily-0003': {
    taskId: 'daily-0003',
    paperId: 'daily-0003',
    type: 'images',
    slides: [],
    totalSlides: 16,  // 实际图片数量
    metadata: {
      paperTitle: 'Meta-Chunking: Learning Text Segmentation and Semantic Completion via Logical Perception',
      generatedAt: '2024-10-16T10:10:00.000Z',
      author: 'Jihao Zhao, Zhiyuan Ji, Yuchen Feng, et al.',
      field: 'Natural Language Processing'
    }
  },

  // 论文4: Efficient Transformer for Image Restoration
  'daily-0004': {
    taskId: 'daily-0004',
    paperId: 'daily-0004',
    type: 'images',
    slides: [],
    totalSlides: 16,  // 实际图片数量
    metadata: {
      paperTitle: 'Comprehensive and Delicate: An Efficient Transformer for Image Restoration',
      generatedAt: '2023-06-01T10:15:00.000Z',
      author: 'Haiyu Zhao, Yuanbiao Gou, Boyun Li, et al.',
      field: 'Computer Vision'
    }
  },

  // 论文5: Multi-Agent Collaborative Reasoning
  'daily-0005': {
    taskId: 'daily-0005',
    paperId: 'daily-0005',
    type: 'images',
    slides: [],
    totalSlides: 16,  // 将根据paperId手动设置
    metadata: {
      paperTitle: 'Multi-Agent Collaborative Reasoning: A Survey of Recent Advances',
      generatedAt: '2025-01-15T10:20:00.000Z',
      author: 'Chen Li, Wu Feng, Huang Kai, Zhang Jun',
      field: 'Artificial Intelligence'
    }
  },

  // 论文6: Chain of Thought Prompting
  'daily-0006': {
    taskId: 'daily-0006',
    paperId: 'daily-0006',
    type: 'images',
    slides: [],
    totalSlides: 14,  // 实际图片数量
    metadata: {
      paperTitle: 'Chain of Thought Prompting: Theoretical Foundations and Learning Dynamics',
      generatedAt: '2025-01-15T10:25:00.000Z',
      author: 'Johnson Emily, Davis Michael, Wilson Sarah',
      field: 'Machine Learning'
    }
  },

  // 论文7: Cultural Understanding in Vision-Language Models
  'daily-0007': {
    taskId: 'daily-0007',
    paperId: 'daily-0007',
    type: 'images',
    slides: [],
    totalSlides: 14,  // 实际图片数量
    metadata: {
      paperTitle: 'Cultural Understanding in Vision-Language Models: A Global Perspective',
      generatedAt: '2025-01-15T10:30:00.000Z',
      author: 'Garcia Maria, Santos Pedro, Rodriguez Carlos',
      field: 'Computer Vision'
    }
  },

  // 论文8: Hallucination Detection in Financial AI
  'daily-0008': {
    taskId: 'daily-0008',
    paperId: 'daily-0008',
    type: 'images',
    slides: [],
    totalSlides: 14,  // 实际图片数量
    metadata: {
      paperTitle: 'Hallucination Detection in Financial AI: Methods and Benchmarks',
      generatedAt: '2025-01-15T10:35:00.000Z',
      author: 'Thompson James, Anderson Lisa, White David',
      field: 'Artificial Intelligence'
    }
  },

  // 历史任务兼容（mock-task-xxx格式）
  // 映射到对应的daily-xxxx
  'mock-task-001': null,  // 重定向到 daily-0001
  'mock-task-002': null,  // 重定向到 daily-0002
  'mock-task-003': null   // Failed task，无内容
}

/**
 * 获取Mock PPT内容
 * @param {string} taskId - 任务ID
 * @returns {Object} PPTContent对象
 * @throws {Error} 如果任务失败（仅当content === null时）
 */
export function getMockPPTContent(taskId) {
  console.log(`[Mock PPT Content] Fetching content for taskId: "${taskId}"`)

  const content = mockPPTContents[taskId]

  // 如果任务明确失败（null），抛出错误
  if (content === null) {
    console.error(`[Mock PPT Content] Task "${taskId}" marked as failed (null)`)
    throw new Error('该任务未成功生成PPT，无法预览')
  }

  // 如果找到精确匹配，返回对应内容
  if (content !== undefined) {
    console.log(`[Mock PPT Content] Found content for taskId "${taskId}":`, content)
    return content
  }

  // 对于未知的taskId，抛出错误而不是返回占位内容
  console.error(`[Mock PPT Content] taskId "${taskId}" not found in mockPPTContents`)
  console.log('[Mock PPT Content] Available taskIds:', Object.keys(mockPPTContents))
  throw new Error(`未找到任务 ${taskId} 的PPT内容`)
}

/**
 * 检查任务是否有预览内容
 * @param {string} taskId - 任务ID
 * @returns {boolean}
 */
export function hasPPTContent(taskId) {
  const content = mockPPTContents[taskId]
  return content !== undefined && content !== null
}

/**
 * 根据paperId获取PPT内容
 * @param {string} paperId - 论文ID
 * @returns {Object|null} PPTContent对象或null
 */
export function getPPTContentByPaperId(paperId) {
  // 遍历找到匹配paperId的内容
  for (const [, content] of Object.entries(mockPPTContents)) {
    if (content && content.paperId === paperId) {
      return content
    }
  }
  return null
}

/**
 * 根据任务对象获取PPT内容（智能查找）
 * 优先使用paperId，fallback到taskId
 * @param {string} taskId - 任务ID
 * @param {Object} task - 任务对象（包含paperId）
 * @returns {Object} PPTContent对象
 * @throws {Error} 如果未找到内容
 */
export function getMockPPTContentByTask(taskId, task = null) {
  console.log(`[Mock PPT Content] Fetching content for taskId: "${taskId}"`, task)

  // 策略1: 如果提供了task对象且有paperId，优先使用paperId查找
  if (task && task.paperId) {
    const contentByPaperId = getPPTContentByPaperId(task.paperId)
    if (contentByPaperId) {
      console.log(`[Mock PPT Content] Found content by paperId "${task.paperId}":`, contentByPaperId)
      return contentByPaperId
    }
  }

  // 策略2: 尝试直接通过taskId查找（用于历史任务）
  const content = mockPPTContents[taskId]
  if (content === null) {
    console.error(`[Mock PPT Content] Task "${taskId}" marked as failed (null)`)
    throw new Error('该任务未成功生成PPT，无法预览')
  }

  if (content !== undefined) {
    console.log(`[Mock PPT Content] Found content by taskId "${taskId}":`, content)
    return content
  }

  // 未找到内容
  console.error(`[Mock PPT Content] No content found for taskId "${taskId}" or paperId "${task?.paperId}"`)
  console.log('[Mock PPT Content] Available taskIds:', Object.keys(mockPPTContents))
  throw new Error(`未找到任务的PPT内容`)
}
