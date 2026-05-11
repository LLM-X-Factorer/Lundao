// Mock data for paper discovery
// Based on real arXiv trending topics in 2025

const generatePaperId = (index, period) => `${period}-${String(index).padStart(4, '0')}`

// Daily trending papers (最新最热门)
export const dailyPapers = [
  {
    id: generatePaperId(1, 'daily'),
    title: 'Addressing Corner Cases in Autonomous Driving: A World Model-based Approach with Mixture of Experts and LLMs',
    authors: ['Haicheng Liao', 'Bonan Wang', 'Junxian Yang', 'Chengyue Wang', 'Zhengbin He', 'Guohui Zhang', 'Chengzhong Xu', 'Zhenning Li'],
    abstract: 'We introduce WM-MoE, a framework that combines world models with mixture-of-experts and LLMs to improve motion forecasting in autonomous vehicles during rare, high-risk corner cases.',
    arxivId: '2510.21867',
    uploadedFileId: null,
    field: 'Computer Vision',
    keywords: ['autonomous driving', 'world models', 'corner cases', 'mixture of experts', 'LLM'],
    publicationDate: '2024-10-29',
    pdfUrl: 'https://arxiv.org/pdf/2510.21867.pdf',
    arxivUrl: 'https://arxiv.org/abs/2510.21867',
    source: 'arxiv'
  },
  {
    id: generatePaperId(2, 'daily'),
    title: 'A Green Multi-Attribute Client Selection for Over-The-Air Federated Learning: A Grey-Wolf-Optimizer Approach',
    authors: ['Maryam Ben Driss', 'Essaid Sabir', 'Halima Elbiaze', 'Abdoulaye Baniré Diallo', 'Mohamed Sadik'],
    abstract: 'We propose a multi-attribute client selection framework for over-the-air federated learning using grey wolf optimizer, balancing accuracy, energy, delay, reliability, and fairness.',
    arxivId: '2409.11442',
    uploadedFileId: null,
    field: 'Machine Learning',
    keywords: ['federated learning', 'client selection', 'optimization', 'energy efficiency', 'fairness'],
    publicationDate: '2024-09-17',
    pdfUrl: 'https://arxiv.org/pdf/2409.11442.pdf',
    arxivUrl: 'https://arxiv.org/abs/2409.11442',
    source: 'arxiv'
  },
  {
    id: generatePaperId(3, 'daily'),
    title: 'Meta-Chunking: Learning Text Segmentation and Semantic Completion via Logical Perception',
    authors: ['Jihao Zhao', 'Zhiyuan Ji', 'Yuchen Feng', 'Pengnian Qi', 'Simin Niu', 'Bo Tang', 'Feiyu Xiong', 'Zhiyu Li'],
    abstract: 'We propose Meta-Chunking, a dual strategy for RAG systems that identifies optimal text segmentation points and preserves global information through adaptive chunking and hierarchical summaries.',
    arxivId: '2410.12788',
    uploadedFileId: null,
    field: 'Natural Language Processing',
    keywords: ['RAG', 'text chunking', 'semantic segmentation', 'information retrieval'],
    publicationDate: '2024-10-16',
    pdfUrl: 'https://arxiv.org/pdf/2410.12788.pdf',
    arxivUrl: 'https://arxiv.org/abs/2410.12788',
    source: 'arxiv'
  },
  {
    id: generatePaperId(4, 'daily'),
    title: 'Comprehensive and Delicate: An Efficient Transformer for Image Restoration',
    authors: ['Haiyu Zhao', 'Yuanbiao Gou', 'Boyun Li', 'Dezhong Peng', 'Jiancheng Lv', 'Xi Peng'],
    abstract: 'We propose an efficient transformer for image restoration that captures superpixel-wise global dependency and transfers it to each pixel, achieving comparable performance with only 6% of SwinIR computational cost.',
    arxivId: 'CVPR2023',
    uploadedFileId: null,
    field: 'Computer Vision',
    keywords: ['image restoration', 'transformer', 'efficiency', 'superpixel', 'attention'],
    publicationDate: '2023-06-01',
    pdfUrl: 'https://openaccess.thecvf.com/content/CVPR2023/papers/Zhao_Comprehensive_and_Delicate_An_Efficient_Transformer_for_Image_Restoration_CVPR_2023_paper.pdf',
    arxivUrl: 'https://openaccess.thecvf.com/content/CVPR2023/html/Zhao_Comprehensive_and_Delicate_An_Efficient_Transformer_for_Image_Restoration_CVPR_2023_paper.html',
    source: 'arxiv'
  },
  {
    id: generatePaperId(5, 'daily'),
    title: 'Multi-Agent Collaborative Reasoning: A Survey of Recent Advances',
    authors: ['Chen Li', 'Wu Feng', 'Huang Kai', 'Zhang Jun'],
    abstract: 'A comprehensive survey of collaborative AI agents, covering reinforcement learning approaches, communication protocols, and emergent behaviors in multi-agent systems.',
    arxivId: '2501.00005',
    uploadedFileId: null,
    field: 'Artificial Intelligence',
    keywords: ['multi-agent', 'collaboration', 'reasoning', 'emergence'],
    publicationDate: '2025-01-14',
    pdfUrl: 'https://arxiv.org/pdf/2501.00005.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00005',
    source: 'arxiv'
  },
  {
    id: generatePaperId(6, 'daily'),
    title: 'Chain of Thought Prompting: Theoretical Foundations and Learning Dynamics',
    authors: ['Johnson Emily', 'Davis Michael', 'Wilson Sarah'],
    abstract: 'We provide theoretical foundations for Chain of Thought prompting, analyzing learning dynamics and proposing improvements based on cognitive science principles.',
    arxivId: '2501.00006',
    uploadedFileId: null,
    field: 'Machine Learning',
    keywords: ['chain of thought', 'prompting', 'theory', 'cognitive science'],
    publicationDate: '2025-01-13',
    pdfUrl: 'https://arxiv.org/pdf/2501.00006.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00006',
    source: 'arxiv'
  },
  {
    id: generatePaperId(7, 'daily'),
    title: 'Cultural Understanding in Vision-Language Models: A Global Perspective',
    authors: ['Garcia Maria', 'Santos Pedro', 'Rodriguez Carlos'],
    abstract: 'Analysis of cultural biases in vision-language models and methods for achieving more inclusive and culturally-aware AI systems across diverse global contexts.',
    arxivId: '2501.00007',
    uploadedFileId: null,
    field: 'Computer Vision',
    keywords: ['cultural AI', 'bias', 'vision-language', 'fairness'],
    publicationDate: '2025-01-13',
    pdfUrl: 'https://arxiv.org/pdf/2501.00007.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00007',
    source: 'arxiv'
  },
  {
    id: generatePaperId(8, 'daily'),
    title: 'Hallucination Detection in Financial AI: Methods and Benchmarks',
    authors: ['Thompson James', 'Anderson Lisa', 'White David'],
    abstract: 'We introduce new benchmarks and detection methods for identifying hallucinations in AI systems applied to financial markets and investment decisions.',
    arxivId: '2501.00008',
    uploadedFileId: null,
    field: 'Artificial Intelligence',
    keywords: ['hallucination', 'finance', 'detection', 'safety'],
    publicationDate: '2025-01-12',
    pdfUrl: 'https://arxiv.org/pdf/2501.00008.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00008',
    source: 'arxiv'
  }
]

// Weekly trending papers (一周热门)
export const weeklyPapers = [
  {
    id: generatePaperId(1, 'weekly'),
    title: 'Diffusion Language Models: Optimization and Reasoning Enhancement',
    authors: ['Liu Yang', 'Chen Xiao', 'Wang Li'],
    abstract: 'Novel approaches to improve reasoning capabilities in diffusion language models through advanced optimization techniques and architectural innovations.',
    arxivId: '2501.00101',
    uploadedFileId: null,
    field: 'Machine Learning',
    keywords: ['diffusion models', 'language models', 'optimization', 'reasoning'],
    publicationDate: '2025-01-10',
    pdfUrl: 'https://arxiv.org/pdf/2501.00101.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00101',
    source: 'arxiv'
  },
  {
    id: generatePaperId(2, 'weekly'),
    title: 'Multi-Scale Neural Operators for Engineering Simulations',
    authors: ['Kumar Priya', 'Singh Arun', 'Patel Raj'],
    abstract: 'Learning multi-scale physics simulations using neural operators, with applications to fluid dynamics, structural analysis, and thermal modeling.',
    arxivId: '2501.00102',
    uploadedFileId: null,
    field: 'Machine Learning',
    keywords: ['neural operators', 'simulation', 'multi-scale', 'physics'],
    publicationDate: '2025-01-09',
    pdfUrl: 'https://arxiv.org/pdf/2501.00102.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00102',
    source: 'arxiv'
  },
  {
    id: generatePaperId(3, 'weekly'),
    title: 'Uncertainty Quantification in Large Language Models: A Bayesian Approach',
    authors: ['Martinez Jose', 'Lopez Ana', 'Fernandez Luis'],
    abstract: 'Bayesian methods for quantifying uncertainty in LLM predictions, enabling more reliable and trustworthy AI-assisted decision making.',
    arxivId: '2501.00103',
    uploadedFileId: null,
    field: 'Artificial Intelligence',
    keywords: ['uncertainty', 'Bayesian', 'LLM', 'reliability'],
    publicationDate: '2025-01-09',
    pdfUrl: 'https://arxiv.org/pdf/2501.00103.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00103',
    source: 'arxiv'
  },
  {
    id: generatePaperId(4, 'weekly'),
    title: 'Deceptive Patterns in User Interfaces: Automated Detection and Prevention',
    authors: ['Cohen Rachel', 'Green Thomas', 'Miller Jennifer'],
    abstract: 'Machine learning approaches to detect and prevent dark patterns and deceptive design in user interfaces, promoting ethical digital experiences.',
    arxivId: '2501.00104',
    uploadedFileId: null,
    field: 'Human-Computer Interaction',
    keywords: ['dark patterns', 'ethics', 'UI/UX', 'detection'],
    publicationDate: '2025-01-08',
    pdfUrl: 'https://arxiv.org/pdf/2501.00104.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00104',
    source: 'arxiv'
  },
  {
    id: generatePaperId(5, 'weekly'),
    title: 'Federated Learning for Healthcare: Privacy-Preserving Disease Prediction',
    authors: ['Zhang Mei', 'Li Wei', 'Wang Qing', 'Chen Hong'],
    abstract: 'Federated learning framework for collaborative disease prediction across hospitals while preserving patient privacy and complying with regulations.',
    arxivId: '2501.00105',
    uploadedFileId: null,
    field: 'Machine Learning',
    keywords: ['federated learning', 'healthcare', 'privacy', 'prediction'],
    publicationDate: '2025-01-08',
    pdfUrl: 'https://arxiv.org/pdf/2501.00105.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00105',
    source: 'arxiv'
  },
  {
    id: generatePaperId(6, 'weekly'),
    title: 'Graph Neural Networks for Materials Discovery',
    authors: ['Kim Yoon', 'Park Seo-Jun', 'Choi Min-Soo'],
    abstract: 'Application of graph neural networks to accelerate materials discovery, predicting properties and stability of novel compounds.',
    arxivId: '2501.00106',
    uploadedFileId: null,
    field: 'Machine Learning',
    keywords: ['GNN', 'materials science', 'discovery', 'prediction'],
    publicationDate: '2025-01-07',
    pdfUrl: 'https://arxiv.org/pdf/2501.00106.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00106',
    source: 'arxiv'
  },
  {
    id: generatePaperId(7, 'weekly'),
    title: 'Robustness and Fairness in Autonomous Driving Systems',
    authors: ['Anderson Eric', 'Taylor Lauren', 'Harris Kevin'],
    abstract: 'Analysis of fairness and robustness issues in autonomous driving perception systems, with proposed methods for bias mitigation.',
    arxivId: '2501.00107',
    uploadedFileId: null,
    field: 'Computer Vision',
    keywords: ['autonomous driving', 'fairness', 'robustness', 'perception'],
    publicationDate: '2025-01-07',
    pdfUrl: 'https://arxiv.org/pdf/2501.00107.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00107',
    source: 'arxiv'
  },
  {
    id: generatePaperId(8, 'weekly'),
    title: 'Explainable AI for Medical Diagnosis: From Black Box to Glass Box',
    authors: ['Brown Patricia', 'Clark Steven', 'Evans Rachel'],
    abstract: 'Methods for creating interpretable and explainable AI systems for medical diagnosis, enabling doctor-AI collaboration and trust.',
    arxivId: '2501.00108',
    uploadedFileId: null,
    field: 'Artificial Intelligence',
    keywords: ['explainability', 'medical AI', 'interpretability', 'diagnosis'],
    publicationDate: '2025-01-06',
    pdfUrl: 'https://arxiv.org/pdf/2501.00108.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00108',
    source: 'arxiv'
  }
]

// Monthly trending papers (一月热门)
export const monthlyPapers = [
  {
    id: generatePaperId(1, 'monthly'),
    title: 'Foundation Models for Robotics: A Comprehensive Survey',
    authors: ['Lee Jae-Sung', 'Park Da-Eun', 'Kim Tae-Woo'],
    abstract: 'Comprehensive survey of foundation models applied to robotics, covering manipulation, navigation, and human-robot interaction.',
    arxivId: '2501.00201',
    uploadedFileId: null,
    field: 'Robotics',
    keywords: ['foundation models', 'robotics', 'survey', 'manipulation'],
    publicationDate: '2025-01-05',
    pdfUrl: 'https://arxiv.org/pdf/2501.00201.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00201',
    source: 'arxiv'
  },
  {
    id: generatePaperId(2, 'monthly'),
    title: 'Efficient Fine-Tuning of Large Language Models: LoRA and Beyond',
    authors: ['Wang Zhi', 'Liu Hua', 'Chen Bo', 'Zhang Kai'],
    abstract: 'Survey and novel methods for parameter-efficient fine-tuning of large language models, with focus on LoRA variants and alternatives.',
    arxivId: '2501.00202',
    uploadedFileId: null,
    field: 'Machine Learning',
    keywords: ['fine-tuning', 'efficiency', 'LoRA', 'LLM'],
    publicationDate: '2025-01-04',
    pdfUrl: 'https://arxiv.org/pdf/2501.00202.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00202',
    source: 'arxiv'
  },
  {
    id: generatePaperId(3, 'monthly'),
    title: 'Neural Architecture Search: From Manual Design to Automated Discovery',
    authors: ['Garcia Miguel', 'Silva Ana', 'Costa Rafael'],
    abstract: 'Evolution of neural architecture search methods, from early manual designs to modern automated approaches using reinforcement learning and evolution.',
    arxivId: '2501.00203',
    uploadedFileId: null,
    field: 'Machine Learning',
    keywords: ['NAS', 'architecture', 'automation', 'evolution'],
    publicationDate: '2025-01-03',
    pdfUrl: 'https://arxiv.org/pdf/2501.00203.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00203',
    source: 'arxiv'
  },
  {
    id: generatePaperId(4, 'monthly'),
    title: 'Contrastive Learning for Self-Supervised Representation',
    authors: ['Tanaka Yuki', 'Suzuki Akira', 'Nakamura Kenji'],
    abstract: 'Novel contrastive learning frameworks for self-supervised representation learning, achieving state-of-the-art results on multiple benchmarks.',
    arxivId: '2501.00204',
    uploadedFileId: null,
    field: 'Machine Learning',
    keywords: ['contrastive learning', 'self-supervised', 'representation', 'SOTA'],
    publicationDate: '2025-01-02',
    pdfUrl: 'https://arxiv.org/pdf/2501.00204.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00204',
    source: 'arxiv'
  },
  {
    id: generatePaperId(5, 'monthly'),
    title: 'Prompt Engineering: A Systematic Survey of Techniques and Applications',
    authors: ['Schmidt Hans', 'Mueller Lisa', 'Weber Thomas'],
    abstract: 'Systematic survey of prompt engineering techniques for large language models, covering zero-shot, few-shot, and chain-of-thought methods.',
    arxivId: '2501.00205',
    uploadedFileId: null,
    field: 'Artificial Intelligence',
    keywords: ['prompt engineering', 'LLM', 'techniques', 'applications'],
    publicationDate: '2025-01-01',
    pdfUrl: 'https://arxiv.org/pdf/2501.00205.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00205',
    source: 'arxiv'
  },
  {
    id: generatePaperId(6, 'monthly'),
    title: 'Attention Mechanisms in Vision Transformers: Analysis and Optimization',
    authors: ['Dubois Marie', 'Bernard Jacques', 'Martin Claire'],
    abstract: 'In-depth analysis of attention mechanisms in vision transformers, with proposed optimizations for improved efficiency and performance.',
    arxivId: '2501.00206',
    uploadedFileId: null,
    field: 'Computer Vision',
    keywords: ['attention', 'vision transformers', 'optimization', 'efficiency'],
    publicationDate: '2024-12-30',
    pdfUrl: 'https://arxiv.org/pdf/2501.00206.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00206',
    source: 'arxiv'
  },
  {
    id: generatePaperId(7, 'monthly'),
    title: 'Quantum Machine Learning: Current Status and Future Directions',
    authors: ['O\'Brien Sean', 'Murphy Fiona', 'Kelly Patrick'],
    abstract: 'Comprehensive review of quantum machine learning algorithms, hardware implementations, and potential applications in various domains.',
    arxivId: '2501.00207',
    uploadedFileId: null,
    field: 'Quantum Computing',
    keywords: ['quantum ML', 'quantum computing', 'algorithms', 'review'],
    publicationDate: '2024-12-29',
    pdfUrl: 'https://arxiv.org/pdf/2501.00207.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00207',
    source: 'arxiv'
  },
  {
    id: generatePaperId(8, 'monthly'),
    title: 'Ethical Considerations in AI Development: A Framework for Responsible Innovation',
    authors: ['Yamamoto Hiro', 'Sato Yuki', 'Ito Mai'],
    abstract: 'Comprehensive framework for ethical AI development, addressing bias, fairness, transparency, and societal impact throughout the AI lifecycle.',
    arxivId: '2501.00208',
    uploadedFileId: null,
    field: 'AI Ethics',
    keywords: ['ethics', 'responsible AI', 'framework', 'society'],
    publicationDate: '2024-12-28',
    pdfUrl: 'https://arxiv.org/pdf/2501.00208.pdf',
    arxivUrl: 'https://arxiv.org/abs/2501.00208',
    source: 'arxiv'
  }
]

// Targeted innovation points for daily papers (Phase 1 - enhanced structure)
const dailyInnovationPoints = {
  'daily-0001': [ // Hierarchical Reasoning Models
    {
      icon: '🚀',
      iconLabel: 'Performance breakthrough',
      title: '27M参数超越大型LLM',
      description: '在Sudoku和ARC-AGI等硬推理任务上，仅2700万参数模型即超越GPT-4等千亿级模型'
    },
    {
      icon: '💡',
      iconLabel: 'Novel approach',
      title: '分层递归推理架构',
      description: '首次提出小规模递归推理方法，通过层次化分解将复杂问题拆解为可管理子任务'
    },
    {
      icon: '⚡',
      iconLabel: 'Efficiency gain',
      title: '训练效率提升50倍',
      description: '相比传统预训练，所需数据量减少99%（仅1000样本），训练时间缩短至2%'
    }
  ],
  'daily-0002': [ // OpenTSLM
    {
      icon: '🌐',
      iconLabel: 'Multimodal integration',
      title: '时间序列原生多模态',
      description: '全球首个将时间序列作为原生模态集成到预训练语言模型的框架'
    },
    {
      icon: '📈',
      iconLabel: 'Forecasting accuracy',
      title: '零样本预测准确率提升20%',
      description: '无需fine-tuning，直接推理任意长度时间序列，预测准确率超越专用模型'
    },
    {
      icon: '🔗',
      iconLabel: 'Cross-modal reasoning',
      title: '跨模态联合推理能力',
      description: '可同时处理文本和多条时间序列，实现跨域知识迁移和复杂因果分析'
    }
  ],
  'daily-0003': [ // Delethink
    {
      icon: '⚡',
      iconLabel: 'Efficiency breakthrough',
      title: '推理路径扩展至10K tokens',
      description: '在超长推理任务中突破二次计算复杂度瓶颈，支持10倍长度推理链'
    },
    {
      icon: '🔬',
      iconLabel: 'Algorithm innovation',
      title: '线性复杂度推理算法',
      description: '创新的删减思考机制将计算复杂度从O(n²)降至O(n log n)，保持推理质量'
    },
    {
      icon: '🎯',
      iconLabel: 'Accuracy maintained',
      title: '长链推理准确率95%',
      description: '在数学推理和逻辑证明任务上，超长推理路径准确率仍保持95%以上'
    }
  ],
  'daily-0004': [ // RLVR
    {
      icon: '🎯',
      iconLabel: 'VQA accuracy',
      title: 'VQA准确率提升8.3%',
      description: '通过可验证奖励机制优化视觉-语言对齐，在多个VQA基准测试上达到新SOTA'
    },
    {
      icon: '🛡️',
      iconLabel: 'Hallucination reduction',
      title: '幻觉检测召回率提升15%',
      description: '可验证奖励信号有效减少视觉推理中的幻觉现象，提高模型可信度'
    },
    {
      icon: '🔄',
      iconLabel: 'Training efficiency',
      title: 'RL训练收敛速度提升3倍',
      description: '相比传统RLHF，可验证奖励机制使强化学习训练收敛速度提升300%'
    }
  ],
  'daily-0005': [ // Multi-Agent Collaborative Reasoning
    {
      icon: '🤝',
      iconLabel: 'Collaboration success',
      title: '协同任务成功率提升40%',
      description: '多智能体协同推理框架在复杂任务分解和并行求解中成功率提升40%'
    },
    {
      icon: '📡',
      iconLabel: 'Communication efficiency',
      title: '通信开销降低60%',
      description: '创新的选择性通信协议减少60%冗余信息交换，保持协同效果'
    },
    {
      icon: '✨',
      iconLabel: 'Emergent behavior',
      title: '涌现协作策略发现',
      description: '观察到未预设的涌现行为，智能体自发形成专业分工和知识互补模式'
    }
  ],
  'daily-0006': [ // Chain of Thought
    {
      icon: '📚',
      iconLabel: 'Theoretical foundation',
      title: '认知科学理论基础构建',
      description: '首次从认知心理学角度系统分析CoT机制，提出5条可验证设计原则'
    },
    {
      icon: '📊',
      iconLabel: 'Performance metrics',
      title: '数学推理准确率89%',
      description: '基于理论优化的CoT方法在GSM8K等数学推理基准上准确率从65%提升至89%'
    },
    {
      icon: '🔍',
      iconLabel: 'Mechanistic insights',
      title: '学习动力学机制解析',
      description: '揭示CoT在fine-tuning过程中的表征学习规律，指导更高效的训练策略'
    }
  ],
  'daily-0007': [ // Cultural Understanding
    {
      icon: '🌍',
      iconLabel: 'Global coverage',
      title: '覆盖50种文化背景测试',
      description: '构建首个大规模多文化视觉-语言理解基准，涵盖五大洲50种文化背景'
    },
    {
      icon: '⚖️',
      iconLabel: 'Bias detection',
      title: '文化偏差检测准确率92%',
      description: '提出自动化文化偏差检测方法，在多个维度（种族、性别、宗教）准确率92%'
    },
    {
      icon: '🔧',
      iconLabel: 'Mitigation methods',
      title: '偏差缓解效果提升35%',
      description: '文化感知微调方法使模型在跨文化任务中的公平性指标提升35%'
    }
  ],
  'daily-0008': [ // Hallucination Detection
    {
      icon: '🎯',
      iconLabel: 'Detection accuracy',
      title: '幻觉检测F1分数0.87',
      description: '在金融领域AI生成内容中，幻觉检测综合准确率达到F1=0.87（精度0.89，召回0.85）'
    },
    {
      icon: '📉',
      iconLabel: 'Error reduction',
      title: '决策错误率降低73%',
      description: '集成幻觉检测机制后，AI驱动的金融投资决策错误率从12%降至3.2%'
    },
    {
      icon: '🔬',
      iconLabel: 'Benchmark contribution',
      title: '发布FinHalluc基准数据集',
      description: '构建包含10万条标注样本的金融幻觉检测基准，覆盖8个子领域'
    }
  ]
}

// Targeted innovation points for weekly papers (Phase 5 - enhanced structure)
const weeklyInnovationPoints = {
  'weekly-0001': [ // Diffusion Language Models
    {
      icon: '🔄',
      iconLabel: 'Model innovation',
      title: '扩散模型用于文本生成',
      description: '首次将扩散过程引入大规模语言建模，在生成质量和多样性之间实现更优平衡'
    },
    {
      icon: '📊',
      iconLabel: 'Performance improvement',
      title: '推理质量提升12%',
      description: '在逻辑推理任务上，扩散语言模型相比标准自回归模型准确率提升12个百分点'
    },
    {
      icon: '⚙️',
      iconLabel: 'Optimization method',
      title: '新型优化算法加速收敛',
      description: '提出针对扩散过程的优化算法，训练收敛速度提升40%，降低计算成本'
    }
  ],
  'weekly-0002': [ // Neural Operators
    {
      icon: '🌊',
      iconLabel: 'Physics simulation',
      title: '多尺度物理仿真突破',
      description: '神经算子可学习跨5个数量级的物理过程，从微观分子到宏观流场统一建模'
    },
    {
      icon: '⚡',
      iconLabel: 'Speed improvement',
      title: '仿真速度提升1000倍',
      description: '相比传统CFD求解器，神经算子在保持精度下将流体仿真速度提升3个数量级'
    },
    {
      icon: '🎯',
      iconLabel: 'Accuracy',
      title: '工程精度达到99.2%',
      description: '在结构分析和热传导任务上，预测误差控制在0.8%以内，满足工程应用标准'
    }
  ],
  'weekly-0003': [ // Uncertainty Quantification
    {
      icon: '📐',
      iconLabel: 'Bayesian framework',
      title: '贝叶斯不确定性量化框架',
      description: '首个针对大型语言模型的完整贝叶斯推理框架，可量化每个token的置信度'
    },
    {
      icon: '🎲',
      iconLabel: 'Calibration',
      title: '校准误差降至5%以内',
      description: '模型置信度与实际准确率的差距从23%缩小至4.7%，大幅提升可信度'
    },
    {
      icon: '🛡️',
      iconLabel: 'Risk detection',
      title: '高风险决策检测率96%',
      description: '在医疗和法律等高风险领域，可提前识别96%的不可靠输出并发出警告'
    }
  ],
  'weekly-0004': [ // Dark Patterns Detection
    {
      icon: '🔍',
      iconLabel: 'Detection capability',
      title: '暗黑模式检测F1=0.89',
      description: '自动化检测系统在12类暗黑模式上综合准确率达F1分数0.89（精度0.91，召回0.87）'
    },
    {
      icon: '🤖',
      iconLabel: 'ML approach',
      title: '多模态检测模型',
      description: '结合视觉特征、文本语义和交互流程的三模态检测模型，覆盖动态欺骗行为'
    },
    {
      icon: '📋',
      iconLabel: 'Dataset',
      title: '构建DarkUI基准数据集',
      description: '收集2.5万个真实网站样本，标注15种暗黑模式类型，为研究提供标准基准'
    }
  ],
  'weekly-0005': [ // Federated Learning Healthcare
    {
      icon: '🔐',
      iconLabel: 'Privacy guarantee',
      title: '差分隐私保护ε=0.1',
      description: '实现严格的差分隐私保证（ε=0.1），在HIPAA合规前提下完成跨院协作'
    },
    {
      icon: '📈',
      iconLabel: 'Prediction accuracy',
      title: '疾病预测AUC提升至0.94',
      description: '联邦学习模型在糖尿病并发症预测上AUC从0.87提升至0.94，接近集中式训练'
    },
    {
      icon: '🏥',
      iconLabel: 'Scale',
      title: '支持百家医院协同训练',
      description: '框架可扩展至100+医疗机构并行训练，通信开销仅为朴素方法的15%'
    }
  ],
  'weekly-0006': [ // GNN for Materials
    {
      icon: '🔬',
      iconLabel: 'Discovery speed',
      title: '材料发现速度提升50倍',
      description: '图神经网络筛选候选材料速度比DFT计算快50倍，大幅加速新材料研发周期'
    },
    {
      icon: '🎯',
      iconLabel: 'Prediction accuracy',
      title: '性能预测MAE=0.03eV',
      description: '在形成能和带隙预测上，平均绝对误差降至0.03eV，达到化学精度要求'
    },
    {
      icon: '💎',
      iconLabel: 'Novel materials',
      title: '发现12种新型稳定材料',
      description: '通过GNN预测并实验验证12种前所未知的稳定晶体结构，其中3种具有商业价值'
    }
  ],
  'weekly-0007': [ // Autonomous Driving Fairness
    {
      icon: '⚖️',
      iconLabel: 'Fairness metrics',
      title: '跨群体公平性提升40%',
      description: '检测率在不同肤色、年龄群体间的差异从28%缩小至6%，显著改善系统公平性'
    },
    {
      icon: '🛡️',
      iconLabel: 'Robustness',
      title: '对抗鲁棒性提升35%',
      description: '在雨雪雾等极端天气条件下，感知系统鲁棒性提升35%，降低安全风险'
    },
    {
      icon: '📊',
      iconLabel: 'Benchmark',
      title: '发布FairDrive基准测试',
      description: '构建包含8种场景、5个人口统计维度的公平性评估基准，已被业界采用'
    }
  ],
  'weekly-0008': [ // Explainable Medical AI
    {
      icon: '🔍',
      iconLabel: 'Interpretability',
      title: '生成临床级解释文本',
      description: '系统可自动生成符合医学规范的诊断推理过程，医生可理解性评分4.6/5.0'
    },
    {
      icon: '🎯',
      iconLabel: 'Diagnostic accuracy',
      title: '诊断准确率提升至93%',
      description: '在10种常见疾病诊断上，可解释模型准确率达93%，与黑盒模型持平且更可信'
    },
    {
      icon: '👨‍⚕️',
      iconLabel: 'Clinical adoption',
      title: '医生采纳率提升60%',
      description: '提供解释后，医生采纳AI建议的比例从45%提升至72%，促进人机协作'
    }
  ]
}

// Targeted innovation points for monthly papers (Phase 5 - enhanced structure)
const monthlyInnovationPoints = {
  'monthly-0001': [ // Foundation Models for Robotics
    {
      icon: '🤖',
      iconLabel: 'Model unification',
      title: '统一操作-导航-交互模型',
      description: '首个将操作、导航、人机交互统一到单一基础模型的机器人系统架构'
    },
    {
      icon: '📊',
      iconLabel: 'Performance',
      title: '任务成功率提升45%',
      description: '在23个机器人基准任务上，基础模型方法相比专用模型平均成功率提升45%'
    },
    {
      icon: '🔄',
      iconLabel: 'Transfer learning',
      title: '跨场景零样本迁移',
      description: '模型可在未见过的环境中实现零样本任务执行，泛化能力提升70%'
    }
  ],
  'monthly-0002': [ // LoRA and Beyond
    {
      icon: '💾',
      iconLabel: 'Parameter efficiency',
      title: '参数量降至0.1%',
      description: 'LoRA++变体仅需微调0.1%参数即可达到全量微调95%的性能，显著降低成本'
    },
    {
      icon: '⚡',
      iconLabel: 'Speed',
      title: '微调速度提升8倍',
      description: '相比全参数微调，训练时间缩短至12.5%，GPU显存占用减少85%'
    },
    {
      icon: '🎯',
      iconLabel: 'Quality',
      title: '下游任务平均提升3.2%',
      description: '在GLUE等17个NLP基准上，新方法相比标准LoRA平均性能提升3.2个百分点'
    }
  ],
  'monthly-0003': [ // Neural Architecture Search
    {
      icon: '🔍',
      iconLabel: 'Search efficiency',
      title: '搜索时间缩短至2小时',
      description: '新型NAS算法在单GPU上2小时内完成架构搜索，效率提升100倍'
    },
    {
      icon: '🏆',
      iconLabel: 'SOTA performance',
      title: '发现5个SOTA架构',
      description: '自动发现的架构在图像分类、目标检测等5个任务上刷新最优性能记录'
    },
    {
      icon: '🌳',
      iconLabel: 'Evolutionary algorithm',
      title: '进化算法收敛速度提升60%',
      description: '结合梯度信息的进化策略使架构搜索收敛代数从500代降至200代'
    }
  ],
  'monthly-0004': [ // Contrastive Learning
    {
      icon: '📈',
      iconLabel: 'Representation quality',
      title: '表征质量提升15%',
      description: '在ImageNet线性评估协议下，新对比学习框架top-1准确率达78.5%，提升15%'
    },
    {
      icon: '🔬',
      iconLabel: 'Theoretical foundation',
      title: '证明对比损失收敛性',
      description: '首次从理论角度证明对比学习在非凸优化下的收敛性质和泛化界'
    },
    {
      icon: '💡',
      iconLabel: 'Novel augmentation',
      title: '自适应增强策略',
      description: '提出根据样本难度自适应调整数据增强强度的方法，性能提升5-8%'
    }
  ],
  'monthly-0005': [ // Prompt Engineering
    {
      icon: '📚',
      iconLabel: 'Comprehensive survey',
      title: '系统总结120种提示技术',
      description: '全面综述零样本、少样本、思维链等120+提示工程技术及其适用场景'
    },
    {
      icon: '🎯',
      iconLabel: 'Best practices',
      title: '提出10条实践原则',
      description: '基于500+实验总结10条提示工程最佳实践，可提升平均任务性能18%'
    },
    {
      icon: '🔧',
      iconLabel: 'Automated optimization',
      title: '自动提示优化工具',
      description: '开发AutoPrompt工具，可自动优化提示模板，平均迭代5轮达到人工水平'
    }
  ],
  'monthly-0006': [ // Vision Transformers
    {
      icon: '👁️',
      iconLabel: 'Attention mechanism',
      title: '稀疏注意力降低75%计算',
      description: '改进的稀疏注意力机制在保持精度下将计算复杂度从O(n²)降至O(n log n)'
    },
    {
      icon: '⚡',
      iconLabel: 'Inference speed',
      title: '推理速度提升3.5倍',
      description: '优化后的ViT在移动设备上推理速度提升350%，实现实时视频处理（30fps）'
    },
    {
      icon: '🎯',
      iconLabel: 'Accuracy',
      title: 'ImageNet准确率85.2%',
      description: '在ImageNet-1K上达到top-1准确率85.2%，超越CNN架构且参数量减少30%'
    }
  ],
  'monthly-0007': [ // Quantum Machine Learning
    {
      icon: '⚛️',
      iconLabel: 'Quantum advantage',
      title: '量子加速比达到100倍',
      description: '在特定优化问题上，量子机器学习算法相比经典算法实现100倍加速'
    },
    {
      icon: '🔬',
      iconLabel: 'Algorithm innovation',
      title: '提出5种新量子算法',
      description: '发明用于分类、聚类、降维的5种变分量子算法，已在真实量子硬件验证'
    },
    {
      icon: '📊',
      iconLabel: 'Hardware progress',
      title: '支持512量子比特系统',
      description: '算法可扩展至512量子比特IBM量子计算机，容错能力提升40%'
    }
  ],
  'monthly-0008': [ // AI Ethics
    {
      icon: '⚖️',
      iconLabel: 'Ethics framework',
      title: '构建6维伦理评估体系',
      description: '提出涵盖公平性、透明度、隐私、问责、安全、社会影响的6维AI伦理框架'
    },
    {
      icon: '🔍',
      iconLabel: 'Bias detection',
      title: '偏差检测覆盖率95%',
      description: '开发的伦理审计工具可检测95%的常见算法偏差，已被12家企业采用'
    },
    {
      icon: '📋',
      iconLabel: 'Policy impact',
      title: '影响3国AI监管政策',
      description: '研究成果被引入欧盟、美国、中国的AI监管政策制定，推动行业自律'
    }
  ]
}

// Mock analysis data generator
export const generateMockAnalysis = (paper) => {
  // Check if this paper has targeted innovation points
  const innovationPoints = dailyInnovationPoints[paper.id] ||
                          weeklyInnovationPoints[paper.id] ||
                          monthlyInnovationPoints[paper.id]

  if (innovationPoints) {
    const summary = `本研究聚焦于${paper.title}。通过${paper.keywords.slice(0, 2).join('和')}等先进技术，团队在${paper.field}领域取得了突破性进展。研究不仅在理论层面提供了深刻洞见，更在实际应用中展现出卓越性能，为该领域的未来发展指明了新方向。`

    return {
      paperId: paper.id,
      chineseSummary: summary,
      innovationPoints: innovationPoints, // Enhanced structure
      analysisTimestamp: new Date().toISOString(),
      analysisStatus: 'completed',
      errorMessage: null
    }
  }

  // Fallback to template-based approach for weekly/monthly papers
  const analysisTemplates = {
    'Machine Learning': {
      summaryPrefix: '本文提出了',
      innovationPoints: [
        '创新性地提出了一种新的模型架构，在多个基准数据集上达到了SOTA性能',
        '通过理论分析证明了方法的收敛性和泛化能力',
        '实验结果表明该方法在计算效率上比现有方法提升了30-50%'
      ]
    },
    'Artificial Intelligence': {
      summaryPrefix: '本研究探讨了',
      innovationPoints: [
        '首次系统性地分析了该问题的理论基础和实践应用',
        '提出了一套完整的解决方案框架，具有广泛的适用性',
        '通过大规模实验验证了方法的有效性和鲁棒性'
      ]
    },
    'Computer Vision': {
      summaryPrefix: '本文针对',
      innovationPoints: [
        '提出了创新的视觉特征提取方法，显著提升了模型性能',
        '设计了高效的网络架构，在保持精度的同时大幅降低了计算成本',
        '在多个视觉任务上取得了突破性进展'
      ]
    },
    'default': {
      summaryPrefix: '本文研究了',
      innovationPoints: [
        '提出了新颖的研究视角和方法论',
        '在理论和实践层面都取得了重要突破',
        '为相关领域的后续研究提供了有价值的参考'
      ]
    }
  }

  const template = analysisTemplates[paper.field] || analysisTemplates.default
  const summary = `${template.summaryPrefix}${paper.title}。研究团队通过${paper.keywords.slice(0, 2).join('和')}技术，解决了该领域的关键问题。主要贡献包括：提出了创新性的模型架构、优化算法和评估方法。实验结果在多个基准数据集上验证了方法的有效性。`

  return {
    paperId: paper.id,
    chineseSummary: summary,
    innovationPoints: template.innovationPoints, // String array (old format)
    analysisTimestamp: new Date().toISOString(),
    analysisStatus: 'completed',
    errorMessage: null
  }
}
