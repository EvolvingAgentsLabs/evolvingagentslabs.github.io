# Image Specifications for Evolving Agents Labs

## Required Images for Website

### 1. Main Project Preview Images
Location: `/images/`

#### **llmunix-preview.png**
- **Size**: 400×240px
- **Format**: PNG
- **Content**: Terminal/code editor view showing LLMunix boot sequence with ASCII art logo
- **Style**: Dark terminal background with green/blue accent colors
- **Text**: Include "LLMunix" logo, "Pure Markdown OS", and some sample agent/tool code
- **Colors**: Dark theme (#1e1e1e background, #00ff00 or #4FC3F7 text)

#### **framework-core-preview.png**
- **Size**: 400×240px
- **Format**: PNG
- **Content**: Architecture diagram showing modular components
- **Style**: Clean, modern diagram with boxes and connections
- **Text**: Include "Framework Core", "Adaptive Behavior", "Memory Systems", "State Management"
- **Colors**: Professional blue/gray theme (#1a73e8, #f8f9fa)

#### **agent-examples-preview.png**
- **Size**: 400×240px
- **Format**: PNG
- **Content**: Grid of small agent icons or workflow diagram
- **Style**: Clean icons representing different agent types
- **Text**: Include "Agent Examples", icons for research, legal, marketing, healthcare
- **Colors**: Consistent with site theme (#1a73e8, #ff6b6b for alpha tags)

#### **eax-router-preview.png**
- **Size**: 400×240px
- **Format**: PNG
- **Content**: Network diagram showing model routing with decision flow
- **Style**: Clean diagram with multiple LLM models and routing logic
- **Text**: Include "EAX Router", "Cost/Latency/Quality", model names (GPT-4, Claude, etc.)
- **Colors**: Blue theme (#1a73e8) with routing arrows and decision nodes

#### **eax-marketplace-preview.png**
- **Size**: 400×240px
- **Format**: PNG
- **Content**: Auction/marketplace visualization with agents bidding
- **Style**: Marketplace interface with bid cards and agent icons
- **Text**: Include "EAX Marketplace", "Task Auction", agent names and bid amounts
- **Colors**: Professional theme with competitive elements (greens for winning bids)

#### **sal-cp-preview.png**
- **Size**: 400×240px
- **Format**: PNG
- **Content**: Communication protocol diagram showing message structure
- **Style**: Technical diagram with message headers and payload visualization
- **Text**: Include "SAL-CP", "Header + Payload", context awareness indicators
- **Colors**: Communication theme (blues and teals) with data flow arrows

### 2. Demo Animation
Location: `/images/`

#### **llmunix-demo.gif**
- **Size**: 800×600px
- **Format**: GIF (optimized, <5MB)
- **Content**: Screen recording of LLMunix boot and task execution
- **Duration**: 10-15 seconds, looping
- **Content**: 
  1. Boot command execution
  2. ASCII art logo appearance
  3. Sample task execution (e.g., web research)
  4. State files being created
  5. Results generation
- **Style**: Terminal/IDE view with syntax highlighting

### 3. Detail Page Images
Location: `/experiments/images/` (optional enhancement)

#### **llmunix-architecture.png**
- **Size**: 800×400px
- **Format**: PNG
- **Content**: Detailed architecture diagram showing state management flow
- **Style**: Technical diagram with arrows and component relationships

#### **adaptive-behavior-diagram.png**
- **Size**: 600×400px
- **Format**: PNG
- **Content**: Flowchart showing constraint adaptation process
- **Style**: Clean flowchart with decision points and feedback loops

### 4. Alpha/Experimental Badges
Location: Inline SVG or small PNG icons

#### **alpha-badge.svg**
- **Size**: 60×20px
- **Format**: SVG
- **Content**: "ALPHA" text with warning icon
- **Colors**: Red background (#ff6b6b), white text

#### **experimental-icon.svg**
- **Size**: 24×24px
- **Format**: SVG
- **Content**: Beaker/lab flask icon
- **Colors**: Match site theme

## Design Guidelines

### Color Palette
- **Primary**: #1a73e8 (Google Blue)
- **Secondary**: #5f6368 (Gray)
- **Background**: #ffffff (White)
- **Accent**: #f8f9fa (Light Gray)
- **Alpha/Warning**: #ff6b6b (Red)
- **Success**: #34a853 (Green)

### Typography
- **Primary Font**: Google Sans
- **Monospace**: Courier New, Monaco, Consolas
- **Sizes**: 
  - Headers: 24-48px
  - Body: 14-16px
  - Code: 12-14px

### Visual Style
- **Modern & Clean**: Minimal design with plenty of whitespace
- **Professional**: Academic/research aesthetic
- **Consistent**: All images should feel cohesive
- **Alpha Emphasis**: Clear experimental/research indicators

### Content Requirements
- All images should include "ALPHA" or "Experimental" indicators
- Avoid production/commercial language
- Include research/lab iconography where appropriate
- Maintain technical accuracy while emphasizing experimental nature

## Tools/Software Recommendations
- **Design**: Figma, Sketch, or Adobe Illustrator
- **Screenshots**: Any screen recording tool
- **GIF Creation**: LICEcap, GIMP, or Photoshop
- **Optimization**: TinyPNG for compression

## File Naming Convention
- Use lowercase with hyphens: `llmunix-preview.png`
- Include dimensions in filename if multiple sizes: `logo-400x240.png`
- Use descriptive names: `adaptive-behavior-diagram.png`

## Fallback Behavior
The CSS includes styled placeholders for missing images:
- Gray background with project name
- Consistent sizing and positioning
- Site functions perfectly without images

## Priority Order
1. **llmunix-preview.png** (Featured project)
2. **eax-router-preview.png** (Key EAX project)
3. **eax-marketplace-preview.png** (Key EAX project)
4. **sal-cp-preview.png** (Key EAX project)
5. **framework-core-preview.png** 
6. **agent-examples-preview.png**
7. **llmunix-demo.gif** (Demo animation)
8. Additional detail images (enhancement)

## Notes
- All images should emphasize the experimental/research nature
- Avoid suggesting production readiness
- Include alpha/experimental indicators where appropriate
- Maintain visual consistency across all images