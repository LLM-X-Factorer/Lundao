/**
 * Mock Historical Task Data
 *
 * Pre-populated task history for demonstrating task states on first app launch
 * These tasks represent completed/failed tasks from "previous" sessions
 */

/**
 * Historical mock tasks (3 tasks: 2 completed + 1 failed)
 * @type {Array<Object>}
 */
export const mockHistoricalTasks = [
  // Task 1: Hierarchical Reasoning Models
  {
    id: 'daily-0001',
    paperId: 'daily-0001',
    paperTitle: 'Hierarchical Reasoning Models: Small-Scale Recursive Reasoning Outperforms LLMs',
    status: 'completed',
    createdAt: '2025-01-15T10:00:00.000Z',
    completedAt: '2025-01-15T10:03:15.000Z',
    downloadUrl: '/ppt-files/daily-0001.pptx',
    progress: 100,
    errorMessage: null,
    retryCount: 0
  },

  // Task 2: OpenTSLM
  {
    id: 'daily-0002',
    paperId: 'daily-0002',
    paperTitle: 'OpenTSLM: Time Series as Native Modality in Pretrained Language Models',
    status: 'completed',
    createdAt: '2025-01-15T10:05:00.000Z',
    completedAt: '2025-01-15T10:08:10.000Z',
    downloadUrl: '/ppt-files/daily-0002.pptx',
    progress: 100,
    errorMessage: null,
    retryCount: 0
  },

  // Task 3: Delethink
  {
    id: 'daily-0003',
    paperId: 'daily-0003',
    paperTitle: 'Delethink: Efficient Very Long Reasoning Without Quadratic Overhead',
    status: 'completed',
    createdAt: '2025-01-15T10:10:00.000Z',
    completedAt: '2025-01-15T10:13:05.000Z',
    downloadUrl: '/ppt-files/daily-0003.pptx',
    progress: 100,
    errorMessage: null,
    retryCount: 0
  },

  // Task 4: RLVR
  {
    id: 'daily-0004',
    paperId: 'daily-0004',
    paperTitle: 'RLVR: Reinforcement Learning with Verifiable Rewards for Vision-Language Models',
    status: 'completed',
    createdAt: '2025-01-15T10:15:00.000Z',
    completedAt: '2025-01-15T10:18:20.000Z',
    downloadUrl: '/ppt-files/daily-0004.pptx',
    progress: 100,
    errorMessage: null,
    retryCount: 0
  },

  // Task 5: Multi-Agent Collaborative Reasoning
  {
    id: 'daily-0005',
    paperId: 'daily-0005',
    paperTitle: 'Multi-Agent Collaborative Reasoning: A Survey of Recent Advances',
    status: 'completed',
    createdAt: '2025-01-15T10:20:00.000Z',
    completedAt: '2025-01-15T10:23:12.000Z',
    downloadUrl: '/ppt-files/daily-0005.pptx',
    progress: 100,
    errorMessage: null,
    retryCount: 0
  },

  // Task 6: Chain of Thought Prompting
  {
    id: 'daily-0006',
    paperId: 'daily-0006',
    paperTitle: 'Chain of Thought Prompting: Theoretical Foundations and Learning Dynamics',
    status: 'completed',
    createdAt: '2025-01-15T10:25:00.000Z',
    completedAt: '2025-01-15T10:28:08.000Z',
    downloadUrl: '/ppt-files/daily-0006.pptx',
    progress: 100,
    errorMessage: null,
    retryCount: 0
  },

  // Task 7: Cultural Understanding in Vision-Language Models
  {
    id: 'daily-0007',
    paperId: 'daily-0007',
    paperTitle: 'Cultural Understanding in Vision-Language Models: A Global Perspective',
    status: 'completed',
    createdAt: '2025-01-15T10:30:00.000Z',
    completedAt: '2025-01-15T10:33:15.000Z',
    downloadUrl: '/ppt-files/daily-0007.pptx',
    progress: 100,
    errorMessage: null,
    retryCount: 0
  },

  // Task 8: Hallucination Detection in Financial AI
  {
    id: 'daily-0008',
    paperId: 'daily-0008',
    paperTitle: 'Hallucination Detection in Financial AI: Methods and Benchmarks',
    status: 'completed',
    createdAt: '2025-01-15T10:35:00.000Z',
    completedAt: '2025-01-15T10:38:22.000Z',
    downloadUrl: '/ppt-files/daily-0008.pptx',
    progress: 100,
    errorMessage: null,
    retryCount: 0
  }
]
