---
paths:
  - frontend/src/**/*.tsx
  - frontend/src/**/*.ts
---

# Frontend Rules — React / TypeScript

## TypeScript

- Always use `unknown` + type guard instead of `any`.
- Always declare shared types in `/types`. Inline types only for local component props.
- Always use `interface` for objects, `type` for unions and intersections.
- Always keep `strict: true` enabled in `tsconfig.json`.

```typescript
interface Task {
  uid: string;
  title: string;
  status: 'todo' | 'in_progress' | 'done';
}
```

## Components

- One component per file. PascalCase name, PascalCase.tsx filename.
- Always use shadcn/ui components (Button, Input, Dialog, etc.) for interactive HTML elements.
- Always place page logic in custom hooks from `/hooks`. Pages only orchestrate.
- Always fetch data via a custom hook from `/hooks`, never directly in a component.

```typescript
export function TaskListPage() {
  const { tasks, isLoading, isError } = useTaskList();
  if (isLoading) return <Spinner />;
  if (isError) return <ErrorMessage />;
  return <TaskList tasks={tasks} />;
}
```

## Data Fetching

- Always use TanStack Query for all server data fetching.
- Always place API functions in `/api`, one file per resource (`tasks.api.ts`).
- Always declare query keys as constants in `/api/query-keys.ts`.
- Always type query errors: `useQuery<Task[], ApiError>`.

```typescript
// /api/tasks.api.ts
export const getTasks = (projectUid: string): Promise<Task[]> =>
  apiClient.get(`/projects/${projectUid}/tasks`).then(r => r.data);

// /hooks/useTaskList.ts
export function useTaskList(projectUid: string) {
  return useQuery({
    queryKey: queryKeys.tasks.byProject(projectUid),
    queryFn: () => getTasks(projectUid),
  });
}
```

## State Management

- Local state (form, modal open): `useState` in the component.
- State shared between nearby components: lift to parent or `useContext`.
- Global app state (current user, current org, notifications): Zustand store in `/store`.
- Always use TanStack Query for server data. Zustand holds client-only state.

## Error Handling

- Always render an explicit error state when `isError` is true.
- Always use React `ErrorBoundary` for unexpected render errors.
- Always show a shadcn/ui `Toast` for mutation errors, not a blocking alert.

## Forms

- Always use `react-hook-form` + `zod` for all forms.
- Always declare the Zod schema in the same file as the form component.
- Always display validation messages inline below each field.

## Accessibility

- Always add `aria-label` to interactive elements whose visible content is an icon only.
- Always add a descriptive `alt` to images. Use `alt=""` only for decorative images.
- Always keep focus coherent after opening/closing a Dialog.

## Performance

- Always use `@tanstack/react-virtual` for lists exceeding 100 items.
- Always import Lucide icons by name: `import { Pencil } from 'lucide-react'`.
- Add `React.memo` only when the profiler shows a real problem, not preemptively.
