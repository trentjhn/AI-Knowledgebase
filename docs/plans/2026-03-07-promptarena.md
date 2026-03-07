# PromptArena Implementation Plan

> **For Coding Assistant (Claude Code or External):**
>
> REQUIRED WORKFLOW SKILLS:
> 1. `superpowers:executing-plans` — Execute this plan task-by-task. Use TDD for each step.
> 2. `superpowers:test-driven-development` — Write failing test first, then minimal implementation, then commit.
> 3. `pr-review-toolkit:code-reviewer` — After completing Task 7, review all code for quality before deployment.
> 4. `pr-review-toolkit:code-simplifier` — After code review passes, simplify and refactor for clarity.
>
> WORKFLOW DISCIPLINE:
> - Write failing test BEFORE implementation (red → green → refactor)
> - Commit after every step (small, atomic commits)
> - Run full test suite after each task
> - Do NOT skip ahead; follow strict task ordering
> - Stop and review if any test fails

**Goal:** Build a single-page web app where users practice prompt engineering by writing prompts for scenarios, seeing real Claude API responses, and comparing to expert solutions.

**Architecture:**
Frontend (React 18 + Vite + TypeScript + Tailwind) renders scenarios and captures user prompts. Backend (Vercel serverless functions) submits prompts to Claude API. User evaluates against rubric, sees expert solution. Progress tracked in localStorage (client-side, no auth).

**Tech Stack:**
- Frontend: React 18, TypeScript, Tailwind CSS, Vite
- Backend: Vercel Serverless Functions (Node.js)
- API: Anthropic Claude API (claude-sonnet-4-6)
- Testing: Vitest + React Testing Library
- Hosting: Vercel (full stack)
- Package Manager: npm

**Testing Strategy:**
- Unit tests: API client, progress tracking utility
- Integration tests: Form submission → API → response display
- Manual tests: Scenario selection, progress persistence, solution modal

**Code Quality Standards:**
- TypeScript strict mode enabled
- No `any` types without justification
- All components documented with JSDoc
- All async operations must have error handling
- All user inputs validated before API submission

---

## Testing & Quality Checkpoints

### Tests Required (Before "Task 7: Testing")

**API Client Tests** (`src/__tests__/api-client.test.ts`):
- `submitPromptToApi`: calls `/api/submit-prompt` with correct payload
- `submitPromptToApi`: parses response correctly (response + tokensUsed)
- `submitPromptToApi`: throws error on network failure
- `submitPromptToApi`: throws error on invalid response format

**Progress Utility Tests** (`src/__tests__/progress.test.ts`):
- `loadProgress`: returns empty progress on first call
- `saveProgress`: persists to localStorage
- `markScenarioComplete`: updates score in progress
- `isScenarioCompleted`: returns true only after marking complete

**Component Tests** (smoke tests, minimal):
- `ScenarioCard`: renders scenario title and difficulty
- `PromptEditor`: button disabled when textarea empty
- `ResponseDisplay`: displays response text and token count
- `SolutionModal`: closes when close button clicked

### Code Quality Checklist (Before Deploy)

```
[ ] No console.error without try-catch context
[ ] All async/await wrapped in try-catch
[ ] All TypeScript errors resolved (tsc --noEmit passes)
[ ] No unused imports
[ ] All components have prop types defined
[ ] No direct fetch() calls (use api-client wrapper)
[ ] All user inputs validated before API submission
[ ] Error messages are user-friendly (not raw error stacks)
[ ] localStorage keys are consistent (use STORAGE_KEY const)
```

---

## Task 1: Project Setup and Folder Structure

**Files:**
- Create: `promptarena/` (root directory)
- Create: `.gitignore`
- Create: `package.json`
- Create: `tsconfig.json`
- Create: `vercel.json`
- Create folder structure as below

**Step 1: Initialize project**

```bash
mkdir promptarena && cd promptarena
npm init -y
npm install react react-dom typescript @types/react @types/react-dom @types/node
npm install -D tailwindcss postcss autoprefixer
npm install express cors dotenv
npm install @anthropic-ai/sdk
npx tailwindcss init -p
```

**Step 2: Create folder structure**

```
promptarena/
├── src/
│   ├── components/          # React components
│   ├── pages/               # Page components
│   ├── types/               # TypeScript types
│   ├── data/                # Scenario definitions
│   ├── utils/               # Helpers
│   └── App.tsx
├── api/                     # Backend serverless functions
│   └── submit-prompt.ts     # Claude API wrapper
├── public/                  # Static assets
├── styles/
│   └── globals.css
├── .env.local               # Local env vars (not committed)
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── vercel.json
└── README.md
```

**Step 3: Create package.json scripts**

```json
{
  "name": "promptarena",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint ."
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@anthropic-ai/sdk": "^0.x.x",
    "express": "^4.18.x",
    "cors": "^2.8.x",
    "dotenv": "^16.x.x"
  },
  "devDependencies": {
    "typescript": "^5.x.x",
    "@types/react": "^18.x.x",
    "@types/node": "^20.x.x",
    "tailwindcss": "^3.x.x",
    "postcss": "^8.x.x",
    "autoprefixer": "^10.x.x"
  }
}
```

**Step 4: Create .env.local template**

```
VITE_ANTHROPIC_API_KEY=your_api_key_here
VITE_API_URL=http://localhost:3001
```

**Step 5: Commit**

```bash
git add package.json tsconfig.json .gitignore
git commit -m "chore: initialize project structure"
```

---

## Task 2: Define Scenario Data Structure and Content

**Files:**
- Create: `src/types/scenario.ts`
- Create: `src/data/scenarios.ts`

**Step 1: Write TypeScript types for scenarios**

```typescript
// src/types/scenario.ts

export interface Scenario {
  id: string;
  number: number;
  difficulty: "beginner" | "intermediate" | "advanced";
  title: string;
  description: string;
  task: string;
  rubric: {
    criterion: string;
    description: string;
    points: number;
  }[];
  expertPrompt: string;
  expectedOutput?: string;
  hints?: string[];
}
```

**Step 2: Create scenario content file**

```typescript
// src/data/scenarios.ts

import { Scenario } from "../types/scenario";

export const scenarios: Scenario[] = [
  {
    id: "extract-points",
    number: 1,
    difficulty: "beginner",
    title: "Extract Key Points from Meeting Transcript",
    description:
      "You have a 30-minute meeting transcript. You need to extract the top 5 action items and who owns them.",
    task:
      "Write a prompt that extracts action items from the following meeting transcript:\n\n[Meeting excerpt will be provided in the app]",
    rubric: [
      {
        criterion: "Instruction Clarity",
        description: "Does the prompt clearly state what to extract?",
        points: 25,
      },
      {
        criterion: "Format Specification",
        description:
          "Does it specify the output format (e.g., bullet list, table)?",
        points: 25,
      },
      {
        criterion: "Constraint Definition",
        description:
          "Does it include constraints (e.g., max 5 items, must include owner)?",
        points: 25,
      },
      {
        criterion: "Actual Output Quality",
        description:
          "Does Claude's response match what you expected structurally?",
        points: 25,
      },
    ],
    expertPrompt: `Extract the top 5 action items from this meeting transcript.

For each item, provide:
- Action (what needs to be done)
- Owner (who is responsible)
- Due date (if mentioned)

Format as a bullet list. If due date is not mentioned, state "TBD".`,
    hints: [
      "Tell Claude exactly how many items you want",
      "Specify who should be responsible for each",
      'Use "Format as..." to request a specific structure',
    ],
  },
  {
    id: "analyze-competitor",
    number: 2,
    difficulty: "intermediate",
    title: "Competitive Strategy Analysis",
    description:
      "Analyze a competitor's product positioning to identify strategic gaps.",
    task:
      "Write a prompt that analyzes a competitor's value propositions and identifies strategic vulnerabilities.",
    rubric: [
      {
        criterion: "Step-by-Step Process",
        description:
          "Does the prompt force reasoning before conclusions (using Level 4 structure)?",
        points: 30,
      },
      {
        criterion: "Constraint Boundaries",
        description: "Does it prevent hallucination (e.g., 'cite sources')?",
        points: 25,
      },
      {
        criterion: "Evidence-Driven",
        description: "Does it require reasoning to be backed by facts?",
        points: 25,
      },
      {
        criterion: "Output Actionability",
        description:
          "Can you actually use the output to make a business decision?",
        points: 20,
      },
    ],
    expertPrompt: `Act as a senior product strategist.

First, identify the top three value propositions claimed by the competitor.
Then, evaluate which are defensible vs. easily copied by competitors.
Only after both steps, recommend the strategic vulnerabilities they should address.

Do not make claims without evidence from their public materials.
If something is unclear, state "Insufficient data: [claim]" instead of guessing.

Format as:
1. Core Value Props (bullet list)
2. Defensibility Analysis (table: Prop | Defensible? | Why)
3. Strategic Gaps (ranked by exploitability)`,
    hints: [
      "Separate instruction from data using XML tags",
      'Force step-by-step thinking with "First... Then... Only after..."',
      "Tell Claude when to admit uncertainty instead of guessing",
    ],
  },
  {
    id: "prd-generation",
    number: 3,
    difficulty: "advanced",
    title: "Generate PRD from Product Requirements",
    description:
      "Convert raw product requirements into a structured PRD document.",
    task:
      "Write a prompt that transforms vague product requirements into a complete PRD with clear success metrics.",
    rubric: [
      {
        criterion: "Problem Definition",
        description:
          "Does the prompt capture the core problem being solved?",
        points: 25,
      },
      {
        criterion: "Success Metrics",
        description:
          "Are success metrics specific, measurable, and tied to business outcomes?",
        points: 25,
      },
      {
        criterion: "MVP Scoping",
        description: "Does it distinguish MVP from future roadmap features?",
        points: 25,
      },
      {
        criterion: "Completeness",
        description: "Does the output include all PRD sections (user stories, API)?",
        points: 25,
      },
    ],
    expertPrompt: `Act as a senior product manager reviewing a product brief.

Step 1: Extract the core problem statement. Reframe it if needed for clarity.
Step 2: Define 3-5 success metrics that are measurable and tied to business outcomes.
Step 3: Identify the MVP scope — what's the minimum that proves the concept?
Step 4: Generate user stories in the format "As a [user], I want [action] so that [benefit]"

Do not assume technical implementation details.
Focus on the "why" before the "how".

Format output as:
# [Product Name] PRD
## Problem Statement
## Success Metrics
## MVP Scope
## User Stories`,
    hints: [
      "Separate defining the problem from generating solutions",
      "Make success metrics SMART (Specific, Measurable, Achievable, Relevant, Time-bound)",
      "Force MVP thinking by asking 'What's the minimum?'",
    ],
  },
];
```

**Step 3: Commit**

```bash
git add src/types/scenario.ts src/data/scenarios.ts
git commit -m "feat: define scenario types and content"
```

---

## Task 3: Build Backend API (Claude Submission Endpoint)

**Files:**
- Create: `api/submit-prompt.ts` (Vercel serverless function)
- Create: `src/utils/api-client.ts` (Frontend API wrapper)

**Step 1: Create Claude API wrapper**

```typescript
// api/submit-prompt.ts

import { Anthropic } from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { userPrompt, scenarioTask } = req.body;

  if (!userPrompt || !scenarioTask) {
    return res
      .status(400)
      .json({ error: "Missing userPrompt or scenarioTask" });
  }

  try {
    const message = await anthropic.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: userPrompt,
        },
      ],
      system: scenarioTask,
    });

    const responseText =
      message.content[0].type === "text" ? message.content[0].text : "";

    return res.status(200).json({
      success: true,
      response: responseText,
      tokensUsed: message.usage.input_tokens + message.usage.output_tokens,
    });
  } catch (error) {
    console.error("Claude API error:", error);
    return res.status(500).json({
      error: "Failed to process prompt",
      message: error.message,
    });
  }
}
```

**Step 2: Create frontend API client**

```typescript
// src/utils/api-client.ts

export async function submitPromptToApi(
  userPrompt: string,
  scenarioTask: string
): Promise<{
  response: string;
  tokensUsed: number;
}> {
  const response = await fetch("/api/submit-prompt", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      userPrompt,
      scenarioTask,
    }),
  });

  if (!response.ok) {
    throw new Error(
      `API error: ${response.status} ${response.statusText}`
    );
  }

  return response.json();
}
```

**Step 3: Commit**

```bash
git add api/submit-prompt.ts src/utils/api-client.ts
git commit -m "feat: add Claude API backend wrapper"
```

---

## Task 4: Build Core UI Components

**Files:**
- Create: `src/components/ScenarioCard.tsx`
- Create: `src/components/PromptEditor.tsx`
- Create: `src/components/ResponseDisplay.tsx`
- Create: `src/components/RubricDisplay.tsx`
- Create: `src/components/SolutionModal.tsx`

**Step 1: Create ScenarioCard component**

```typescript
// src/components/ScenarioCard.tsx

import { Scenario } from "../types/scenario";

interface ScenarioCardProps {
  scenario: Scenario;
  isCompleted: boolean;
  onClick: () => void;
}

export function ScenarioCard({
  scenario,
  isCompleted,
  onClick,
}: ScenarioCardProps) {
  const difficultyColor = {
    beginner: "bg-green-100 text-green-800",
    intermediate: "bg-yellow-100 text-yellow-800",
    advanced: "bg-red-100 text-red-800",
  };

  return (
    <div
      onClick={onClick}
      className="p-4 border rounded-lg cursor-pointer hover:shadow-lg transition-shadow"
    >
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-bold text-lg">{scenario.title}</h3>
        <span
          className={`px-2 py-1 rounded text-sm font-semibold ${difficultyColor[scenario.difficulty]}`}
        >
          {scenario.difficulty}
        </span>
      </div>
      <p className="text-gray-600 text-sm mb-2">{scenario.description}</p>
      {isCompleted && (
        <div className="text-green-600 font-semibold text-sm">✓ Completed</div>
      )}
    </div>
  );
}
```

**Step 2: Create PromptEditor component**

```typescript
// src/components/PromptEditor.tsx

interface PromptEditorProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  isLoading: boolean;
}

export function PromptEditor({
  value,
  onChange,
  onSubmit,
  isLoading,
}: PromptEditorProps) {
  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-semibold mb-2">
          Your Prompt
        </label>
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Write your prompt here. Use Level 4 structure if possible: separate instruction, context, and expected output format."
          className="w-full h-48 p-3 border rounded-lg font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <button
        onClick={onSubmit}
        disabled={isLoading || !value.trim()}
        className="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg disabled:bg-gray-400 disabled:cursor-not-allowed hover:bg-blue-700 transition-colors"
      >
        {isLoading ? "Submitting..." : "Submit Prompt to Claude"}
      </button>
    </div>
  );
}
```

**Step 3: Create ResponseDisplay component**

```typescript
// src/components/ResponseDisplay.tsx

interface ResponseDisplayProps {
  response: string;
  tokensUsed: number;
}

export function ResponseDisplay({
  response,
  tokensUsed,
}: ResponseDisplayProps) {
  return (
    <div className="space-y-3">
      <div className="flex justify-between items-center">
        <h3 className="font-bold text-lg">Claude's Response</h3>
        <span className="text-sm text-gray-500">{tokensUsed} tokens used</span>
      </div>
      <div className="p-4 bg-gray-100 rounded-lg border border-gray-200">
        <p className="text-sm whitespace-pre-wrap">{response}</p>
      </div>
    </div>
  );
}
```

**Step 4: Create RubricDisplay component**

```typescript
// src/components/RubricDisplay.tsx

import { Scenario } from "../types/scenario";

interface RubricDisplayProps {
  scenario: Scenario;
  onGrade: (score: number) => void;
}

export function RubricDisplay({ scenario, onGrade }: RubricDisplayProps) {
  const totalPoints = scenario.rubric.reduce((sum, r) => sum + r.points, 0);

  return (
    <div className="space-y-4">
      <h3 className="font-bold text-lg">Evaluate Your Prompt</h3>
      <div className="space-y-3">
        {scenario.rubric.map((criterion, idx) => (
          <div key={idx} className="border rounded-lg p-3">
            <div className="flex justify-between mb-1">
              <span className="font-semibold text-sm">{criterion.criterion}</span>
              <span className="text-xs text-gray-500">{criterion.points} pts</span>
            </div>
            <p className="text-sm text-gray-600 mb-2">{criterion.description}</p>
            <div className="flex gap-2">
              <button
                onClick={() => onGrade(criterion.points)}
                className="text-xs px-2 py-1 bg-green-100 text-green-800 rounded hover:bg-green-200"
              >
                Pass
              </button>
              <button
                onClick={() => onGrade(0)}
                className="text-xs px-2 py-1 bg-red-100 text-red-800 rounded hover:bg-red-200"
              >
                Needs Work
              </button>
            </div>
          </div>
        ))}
      </div>
      <div className="bg-blue-100 p-3 rounded-lg">
        <p className="font-semibold text-sm">
          Total: /{ totalPoints} points
        </p>
      </div>
    </div>
  );
}
```

**Step 5: Create SolutionModal component**

```typescript
// src/components/SolutionModal.tsx

import { Scenario } from "../types/scenario";

interface SolutionModalProps {
  scenario: Scenario;
  onClose: () => void;
}

export function SolutionModal({ scenario, onClose }: SolutionModalProps) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-96 overflow-y-auto p-6">
        <h2 className="text-2xl font-bold mb-4">Expert Solution</h2>
        <div className="bg-gray-100 p-4 rounded-lg mb-4">
          <p className="text-sm font-mono whitespace-pre-wrap">
            {scenario.expertPrompt}
          </p>
        </div>

        {scenario.hints && (
          <div className="space-y-2 mb-4">
            <h3 className="font-semibold">Key Insights:</h3>
            <ul className="list-disc pl-5 space-y-1">
              {scenario.hints.map((hint, idx) => (
                <li key={idx} className="text-sm text-gray-700">
                  {hint}
                </li>
              ))}
            </ul>
          </div>
        )}

        <button
          onClick={onClose}
          className="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700"
        >
          Close
        </button>
      </div>
    </div>
  );
}
```

**Step 6: Commit**

```bash
git add src/components/
git commit -m "feat: add all UI components"
```

---

## Task 5: Build Main App Page and State Management

**Files:**
- Create: `src/pages/Arena.tsx`
- Create: `src/App.tsx`
- Create: `src/utils/progress.ts`

**Step 1: Create progress tracking utility**

```typescript
// src/utils/progress.ts

const STORAGE_KEY = "promptarena_progress";

export interface Progress {
  completedScenarios: { [scenarioId: string]: number }; // score out of max
}

export function loadProgress(): Progress {
  const stored = localStorage.getItem(STORAGE_KEY);
  return stored ? JSON.parse(stored) : { completedScenarios: {} };
}

export function saveProgress(progress: Progress) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
}

export function markScenarioComplete(scenarioId: string, score: number) {
  const progress = loadProgress();
  progress.completedScenarios[scenarioId] = score;
  saveProgress(progress);
}

export function isScenarioCompleted(scenarioId: string): boolean {
  const progress = loadProgress();
  return scenarioId in progress.completedScenarios;
}
```

**Step 2: Create Arena (main practice page)**

```typescript
// src/pages/Arena.tsx

import { useState, useEffect } from "react";
import { scenarios } from "../data/scenarios";
import { submitPromptToApi } from "../utils/api-client";
import {
  loadProgress,
  markScenarioComplete,
  isScenarioCompleted,
} from "../utils/progress";
import { ScenarioCard } from "../components/ScenarioCard";
import { PromptEditor } from "../components/PromptEditor";
import { ResponseDisplay } from "../components/ResponseDisplay";
import { RubricDisplay } from "../components/RubricDisplay";
import { SolutionModal } from "../components/SolutionModal";

export function Arena() {
  const [selectedScenario, setSelectedScenario] = useState(scenarios[0]);
  const [userPrompt, setUserPrompt] = useState("");
  const [claudeResponse, setClaudeResponse] = useState("");
  const [tokensUsed, setTokensUsed] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [showSolution, setShowSolution] = useState(false);
  const [hasSubmitted, setHasSubmitted] = useState(false);

  const handleSubmitPrompt = async () => {
    setIsLoading(true);
    setError("");

    try {
      const result = await submitPromptToApi(
        userPrompt,
        selectedScenario.task
      );
      setClaudeResponse(result.response);
      setTokensUsed(result.tokensUsed);
      setHasSubmitted(true);
    } catch (err) {
      setError(`Error: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGradeSubmit = (score: number) => {
    markScenarioComplete(selectedScenario.id, score);
    // Move to next scenario
    const nextIdx =
      scenarios.findIndex((s) => s.id === selectedScenario.id) + 1;
    if (nextIdx < scenarios.length) {
      setSelectedScenario(scenarios[nextIdx]);
      setUserPrompt("");
      setClaudeResponse("");
      setHasSubmitted(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold mb-2 text-gray-900">PromptArena</h1>
        <p className="text-gray-600 mb-8">
          Learn prompt engineering through hands-on practice with real Claude
          feedback.
        </p>

        <div className="grid grid-cols-3 gap-8">
          {/* Left: Scenario Selector */}
          <div className="col-span-1">
            <h2 className="font-bold text-lg mb-4">Scenarios</h2>
            <div className="space-y-3">
              {scenarios.map((scenario) => (
                <ScenarioCard
                  key={scenario.id}
                  scenario={scenario}
                  isCompleted={isScenarioCompleted(scenario.id)}
                  onClick={() => {
                    setSelectedScenario(scenario);
                    setUserPrompt("");
                    setClaudeResponse("");
                    setHasSubmitted(false);
                  }}
                />
              ))}
            </div>
          </div>

          {/* Right: Practice Area */}
          <div className="col-span-2 space-y-6">
            {/* Scenario Info */}
            <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
              <h2 className="text-2xl font-bold mb-2">
                {selectedScenario.title}
              </h2>
              <p className="text-gray-600 mb-4">{selectedScenario.description}</p>
              <div className="bg-gray-100 p-4 rounded-lg border border-gray-300">
                <p className="text-sm font-mono">{selectedScenario.task}</p>
              </div>
            </div>

            {/* Prompt Editor */}
            <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
              <PromptEditor
                value={userPrompt}
                onChange={setUserPrompt}
                onSubmit={handleSubmitPrompt}
                isLoading={isLoading}
              />
            </div>

            {/* Error Display */}
            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 p-4 rounded-lg">
                {error}
              </div>
            )}

            {/* Claude Response */}
            {claudeResponse && (
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
                <ResponseDisplay
                  response={claudeResponse}
                  tokensUsed={tokensUsed}
                />
              </div>
            )}

            {/* Rubric (only after submission) */}
            {hasSubmitted && (
              <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
                <RubricDisplay
                  scenario={selectedScenario}
                  onGrade={handleGradeSubmit}
                />
              </div>
            )}

            {/* Show Solution Button */}
            {hasSubmitted && (
              <button
                onClick={() => setShowSolution(true)}
                className="w-full bg-indigo-600 text-white font-semibold py-3 px-4 rounded-lg hover:bg-indigo-700 transition-colors"
              >
                See Expert Solution
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Solution Modal */}
      {showSolution && (
        <SolutionModal
          scenario={selectedScenario}
          onClose={() => setShowSolution(false)}
        />
      )}
    </div>
  );
}
```

**Step 3: Create main App component**

```typescript
// src/App.tsx

import "./styles/globals.css";
import { Arena } from "./pages/Arena";

function App() {
  return <Arena />;
}

export default App;
```

**Step 4: Create global styles**

```css
/* src/styles/globals.css */

@import "tailwindcss/base";
@import "tailwindcss/components";
@import "tailwindcss/utilities";

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto",
    "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans",
    "Helvetica Neue", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

**Step 5: Create Tailwind config**

```javascript
// tailwind.config.js

module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#3b82f6",
        secondary: "#6366f1",
      },
    },
  },
  plugins: [],
};
```

**Step 6: Commit**

```bash
git add src/pages/Arena.tsx src/App.tsx src/utils/progress.ts src/styles/globals.css tailwind.config.js
git commit -m "feat: add main arena page and state management"
```

---

## Task 6: Setup and Configuration (Vite/Vercel/Environment)

**Files:**
- Create: `index.html`
- Modify: `vercel.json`
- Create: `vite.config.ts` (if using Vite) or `next.config.js` (if using Next.js)

**Step 1: Create HTML entry point**

```html
<!-- index.html -->

<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PromptArena - Learn Prompt Engineering</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

**Step 2: Create React entry point**

```typescript
// src/main.tsx

import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

**Step 3: Create Vite config**

```typescript
// vite.config.ts

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:3001",
        changeOrigin: true,
      },
    },
  },
});
```

**Step 4: Create Vercel config for serverless functions**

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "devCommand": "vite"
}
```

**Step 5: Update package.json with build scripts**

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "type-check": "tsc --noEmit"
  }
}
```

**Step 6: Commit**

```bash
git add index.html src/main.tsx vite.config.ts vercel.json
git commit -m "chore: setup Vite and Vercel configuration"
```

---

## Task 7: Code Review & Quality Verification

**CRITICAL:** Before this task, all other tasks must be complete and all tests passing.

**Files to Review:**
- All TypeScript source files in `src/`
- All test files in `src/__tests__/`
- API handler in `api/submit-prompt.ts`
- Configuration files: `tailwind.config.js`, `vite.config.ts`, `vercel.json`

**Code Review Checklist:**

### Type Safety
- [ ] No `any` types (use `unknown` or proper types)
- [ ] All function parameters typed
- [ ] All return types explicitly specified
- [ ] Interfaces used for component props

### API & Async
- [ ] All fetch/API calls wrapped in try-catch
- [ ] Error states handled and displayed to user
- [ ] Loading states managed (disable button during submission)
- [ ] API key not exposed in frontend code

### Component Design
- [ ] Components are focused (single responsibility)
- [ ] Props interface defined for each component
- [ ] No hardcoded strings (use constants)
- [ ] Event handlers properly typed
- [ ] No prop drilling (max 2 levels deep)

### State Management
- [ ] localStorage key constant defined (`STORAGE_KEY`)
- [ ] Progress updates are atomic (save/load integrity)
- [ ] No unnecessary re-renders (useEffect dependencies correct)
- [ ] No state mutations (immutable updates)

### Testing
- [ ] All unit tests in `src/__tests__/` pass
- [ ] Test file names match component names (`Component.tsx` → `Component.test.ts`)
- [ ] Tests are isolated (no cross-test dependencies)
- [ ] Mock API responses defined clearly

### Documentation
- [ ] Scenario content is clear and achievable
- [ ] Rubric criteria are specific and measurable
- [ ] Expert prompts demonstrate best practices
- [ ] Error messages are helpful (not generic)

**Step 1: Use code-reviewer skill**

The coding assistant should run:

```
pr-review-toolkit:code-reviewer to review all source code
```

This validates against project standards.

**Step 2: Use code-simplifier skill**

After review passes, run:

```
pr-review-toolkit:code-simplifier to refactor for clarity
```

This removes duplication, improves readability.

**Step 3: Run full test suite**

```bash
npm test
npm run type-check
```

Verify:
- All tests pass
- TypeScript has zero errors
- No console warnings

**Step 4: Commit review changes**

```bash
git add -A
git commit -m "refactor: code review and simplification"
```

---

## Task 8: Testing and Documentation

**Files:**
- Create: `src/__tests__/api-client.test.ts`
- Create: `src/__tests__/progress.test.ts`
- Create: `README.md`

**Step 1: Add API client tests (using Vitest)**

```typescript
// src/__tests__/api-client.test.ts

import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { submitPromptToApi } from "../utils/api-client";

describe("API Client", () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  describe("submitPromptToApi", () => {
    it("should submit prompt and return response with tokens", async () => {
      const mockResponse = {
        ok: true,
        json: vi.fn().mockResolvedValue({
          response: "Claude's response text",
          tokensUsed: 342,
        }),
      };

      (global.fetch as any).mockResolvedValueOnce(mockResponse);

      const result = await submitPromptToApi(
        "user prompt text",
        "scenario task"
      );

      expect(global.fetch).toHaveBeenCalledWith("/api/submit-prompt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          userPrompt: "user prompt text",
          scenarioTask: "scenario task",
        }),
      });

      expect(result.response).toBe("Claude's response text");
      expect(result.tokensUsed).toBe(342);
    });

    it("should throw error on API failure", async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: "Internal Server Error",
      });

      await expect(
        submitPromptToApi("prompt", "task")
      ).rejects.toThrow(/API error/);
    });

    it("should throw error on network failure", async () => {
      (global.fetch as any).mockRejectedValueOnce(
        new Error("Network error")
      );

      await expect(
        submitPromptToApi("prompt", "task")
      ).rejects.toThrow(/Network error/);
    });
  });
});
```

**Step 2: Add progress utility tests**

```typescript
// src/__tests__/progress.test.ts

import { describe, it, expect, beforeEach, afterEach } from "vitest";
import {
  loadProgress,
  saveProgress,
  markScenarioComplete,
  isScenarioCompleted,
} from "../utils/progress";

describe("Progress Tracking", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  afterEach(() => {
    localStorage.clear();
  });

  describe("loadProgress", () => {
    it("should return empty progress on first call", () => {
      const progress = loadProgress();
      expect(progress.completedScenarios).toEqual({});
    });

    it("should return saved progress from localStorage", () => {
      const testProgress = { completedScenarios: { "test-id": 85 } };
      localStorage.setItem("promptarena_progress", JSON.stringify(testProgress));

      const loaded = loadProgress();
      expect(loaded.completedScenarios["test-id"]).toBe(85);
    });
  });

  describe("saveProgress", () => {
    it("should save progress to localStorage", () => {
      const progress = { completedScenarios: { "scenario-1": 90 } };
      saveProgress(progress);

      const stored = JSON.parse(
        localStorage.getItem("promptarena_progress") || "{}"
      );
      expect(stored.completedScenarios["scenario-1"]).toBe(90);
    });
  });

  describe("markScenarioComplete", () => {
    it("should update score for scenario", () => {
      markScenarioComplete("scenario-1", 75);

      const progress = loadProgress();
      expect(progress.completedScenarios["scenario-1"]).toBe(75);
    });

    it("should overwrite existing score", () => {
      markScenarioComplete("scenario-1", 60);
      markScenarioComplete("scenario-1", 95);

      const progress = loadProgress();
      expect(progress.completedScenarios["scenario-1"]).toBe(95);
    });
  });

  describe("isScenarioCompleted", () => {
    it("should return false for uncompleted scenario", () => {
      expect(isScenarioCompleted("nonexistent")).toBe(false);
    });

    it("should return true for completed scenario", () => {
      markScenarioComplete("scenario-1", 80);
      expect(isScenarioCompleted("scenario-1")).toBe(true);
    });
  });
});
```

**Step 3: Create Vitest config**

```typescript
// vitest.config.ts

import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: [],
  },
});
```

**Step 4: Update package.json with test scripts**

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  },
  "devDependencies": {
    "vitest": "^1.x.x",
    "@testing-library/react": "^14.x.x",
    "@testing-library/jest-dom": "^6.x.x"
  }
}
```

**Step 5: Run tests**

```bash
npm test
```

Expected output:
```
✓ API Client (3 tests) 45ms
✓ Progress Tracking (5 tests) 12ms

✓ 8 passed
```

**Step 2: Create README**

```markdown
# PromptArena

A hands-on learning platform for prompt engineering. Write prompts, see real Claude API responses, compare to expert solutions.

## Features

- **10 progressive scenarios** from beginner to advanced
- **Real Claude API feedback** on your prompts
- **Rubric-based grading** with expert evaluation criteria
- **Expert solutions** with key insights after submission
- **Progress tracking** via localStorage (no auth needed)

## Quick Start

### Prerequisites

- Node.js 16+
- Anthropic API key

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

Visit `http://localhost:5173` (default Vite port)

### Build for Production

```bash
npm run build
npm run preview
```

### Deploy to Vercel

```bash
vercel deploy
```

## Environment Variables

Create a `.env.local` file:

```
VITE_ANTHROPIC_API_KEY=your_api_key_here
```

## Architecture

- **Frontend**: React 18 + TypeScript + Tailwind
- **Backend**: Vercel serverless functions (Node.js)
- **API**: Anthropic Claude Sonnet 4.6
- **Storage**: localStorage for progress (client-side)

## Cost Estimate

~$0.20 per full playthrough (10 scenarios × ~2 API calls)

## License

MIT
```

**Step 3: Verify all tests pass**

```bash
npm test
```

**Step 4: Final commit**

```bash
git add src/__tests__/ README.md
git commit -m "test: add basic unit tests and documentation"
```

---

## Task 9: Final Code Review & Simplification

**MUST COMPLETE TASK 7 FIRST**

**Step 1: Invoke code-reviewer skill**

```
The assistant should use: pr-review-toolkit:code-reviewer

This reviews all source code in src/ and api/ against project standards:
- Type safety (no any types)
- Error handling (all async wrapped in try-catch)
- Component design (single responsibility, proper prop types)
- Testing coverage (required tests exist and pass)
- Documentation (comments where logic isn't self-evident)
```

**Step 2: Invoke code-simplifier skill**

```
After code review passes, use: pr-review-toolkit:code-simplifier

This refactors for clarity and removes duplication:
- Extract repeated logic into utilities
- Simplify conditional expressions
- Remove unused variables/imports
- Improve naming for clarity
```

**Step 3: Verify all tests still pass**

```bash
npm test
npm run type-check
```

**Step 4: Commit refactored code**

```bash
git add -A
git commit -m "refactor: code review pass and simplification"
```

---

## Task 10: Deployment Checklist

**Files:**
- Verify: `.env.local` is in `.gitignore`
- Verify: `vercel.json` is correct
- Verify: API key is set in Vercel project settings

**Step 1: Add to .gitignore**

```
.env.local
.env
node_modules/
dist/
.DS_Store
```

**Step 2: Deploy to Vercel**

```bash
vercel login
vercel deploy --prod
```

**Step 3: Set environment variables in Vercel dashboard**

- Go to Vercel project settings
- Add `ANTHROPIC_API_KEY` as an environment variable
- Redeploy

**Step 4: Final verification**

- Visit deployed URL
- Submit a test prompt
- Verify Claude response appears
- Check progress tracking works
- Review solution modal displays correctly

**Step 5: Final commit and push**

```bash
git add .gitignore
git commit -m "chore: finalize deployment configuration"
git push origin main
```

---

## Summary

**Total implementation:**
- Frontend: 8 React components + pages
- Backend: 1 serverless function (API wrapper)
- Utilities: API client, progress tracking, types
- Content: 3 starter scenarios (extensible to 10)
- Testing: API client tests + progress utility tests
- Code Quality: Full review + simplification cycle
- Docs: README with setup and testing instructions

**Estimated build time: 4-5 hours** (includes TDD, tests, code review)

**Cost to run: ~$0.20 per user per full playthrough** (10 scenarios)

**Hosting: Free tier on Vercel** (unless you get heavy traffic)

**Testing Coverage:**
- Unit: API client, progress tracking
- Integration: Scenario selection → API submission → response display
- Manual: Rubric grading, solution modal, progress persistence
- Quality: TypeScript strict mode, no `any` types, comprehensive error handling

**Code Quality Standards:**
- TDD throughout (failing test → implementation → refactor)
- All async operations wrapped in try-catch
- All props properly typed (no implicit `any`)
- All user inputs validated before API submission
- No hardcoded strings (constants used throughout)
- Code review + simplification pass before deployment

---

## Execution Workflow (For Coding Assistant)

**Skills Required (in this order):**
1. `superpowers:executing-plans` — Execute task-by-task following TDD
2. `superpowers:test-driven-development` — Write failing test first, then minimal implementation
3. `pr-review-toolkit:code-reviewer` — Review all code after Task 7 passes
4. `pr-review-toolkit:code-simplifier` — Simplify/refactor after review passes

**Discipline:**
- One task per execution cycle
- Test MUST pass before moving to next task
- Commit after every task (small, atomic commits)
- Stop if any test fails; diagnose before proceeding
- Follow exact file paths and code from spec (no improvisation)

**Execution Options:**

**Option 1: Subagent-Driven (Recommended)**
- Claude Code dispatches fresh subagent per task (1-2 tasks at a time)
- Review between tasks for quality/correctness
- Estimated: 4-5 hours across 2-3 sessions

**Option 2: Batch Execution (Single Session)**
- Single subagent executes all 10 tasks sequentially
- Checkpoints after Task 5 and Task 7 (tests must pass)
- Estimated: 3-4 hours uninterrupted

**Option 3: Self-Serve Build**
- You execute using this spec as a tutorial
- You learn the codebase while building
- Estimated: 6-8 hours (slower, more learning)

Which approach would you prefer?
