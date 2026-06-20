---
paths:
  - backend/src/**/*.ts
---

# Backend Rules — Node.js / NestJS

## Public Identifiers (IDOR Security)

- Always use `publicId: string` (UUID v4) in URLs and response DTOs.
- Always declare `@Param('taskUid', ParseUUIDPipe) taskUid: string` in controllers. Keep integer `id` internal to the persistence layer only.
- Always resolve `publicId → internal id` as the first step in the service method.

```typescript
@Get(':taskUid')
@UseGuards(JwtAuthGuard)
findOne(@Param('taskUid', ParseUUIDPipe) taskUid: string, @CurrentUser() user: AuthUser) {
  return this.tasksService.findByPublicId(taskUid, user.organizationId);
}
```

## Module Boundaries

- Always organize one domain per NestJS module: `TasksModule`, `ProjectsModule`, `AuthModule`.
- Always declare dependencies in `@Module({ imports: [...], providers: [...], exports: [...] })`.
- Always import another module to use its exported providers. Never import a service file directly from another module's folder.
- Always export services that other modules need via the module's `exports` array.

```typescript
@Module({
  imports: [TypeOrmModule.forFeature([TaskEntity]), ProjectsModule],
  controllers: [TasksController],
  providers: [TasksService],
  exports: [TasksService],
})
export class TasksModule {}
```

## Dependency Injection

- Always annotate services with `@Injectable()` and inject dependencies via constructor.
- Never instantiate services with `new TasksService()`.
- Always register providers in the module's `providers` array or a dedicated `providers/` export.

```typescript
@Injectable()
export class TasksService {
  constructor(
    @InjectRepository(TaskEntity) private readonly taskRepo: Repository<TaskEntity>,
    private readonly projectsService: ProjectsService,
  ) {}
}
```

## Layered Architecture

- Always follow: `Controller → Service → Repository`. No layer skipping.
- Controllers validate DTOs, call services, return results. No business logic or entity mapping.
- Services hold all business logic. No direct query building beyond delegating to repositories.
- Repositories (TypeORM `Repository<T>` or custom `@Injectable()` repository classes) hold query logic.

## Controllers

- Always use `@Controller('api/v1/tasks')` with versioned prefix.
- Always type `@Body()` with a DTO class. Never use `Record<string, unknown>` or `any`.
- Always protect routes with `@UseGuards(JwtAuthGuard)` unless explicitly public. Combine `@Roles('ADMIN')` with `RolesGuard` for role-based access.
- Always extract `organizationId` from JWT via `@CurrentUser()` — never from the request body.
- Never map entities to response DTOs in controllers — delegate to service or interceptor.

```typescript
@Post()
@HttpCode(HttpStatus.CREATED)
@UseGuards(JwtAuthGuard)
create(@Body() dto: CreateTaskDto, @CurrentUser() user: AuthUser) {
  return this.tasksService.create(dto, user);
}
```

## DTOs & Validation

- Always decorate DTO properties with `class-validator` decorators (`@IsString`, `@IsUUID`, `@MaxLength`, etc.).
- Always enable global `ValidationPipe` with `whitelist: true`, `forbidNonWhitelisted: true`, `transform: true`.
- Always use separate request and response DTOs. Never return TypeORM entities from controllers.

```typescript
export class CreateTaskDto {
  @IsString()
  @MaxLength(255)
  title: string;

  @IsUUID()
  projectPublicId: string;
}
```

## Services

- Always throw typed domain exceptions (`TaskNotFoundException`) when a resource is not found.
- Always filter on `organizationId` in every multi-tenant query.
- Always return response DTOs or plain objects — never TypeORM entities.

```typescript
async findByPublicId(publicId: string, organizationId: number): Promise<TaskResponseDto> {
  const task = await this.taskRepo.findOne({ where: { publicId, organizationId } });
  if (!task) throw new TaskNotFoundException(publicId);
  return this.mapper.toResponse(task);
}
```

## Interceptors & Filters

- Always map entity → response DTO in a `ClassSerializerInterceptor`, custom `TransformInterceptor`, or dedicated mapper class.
- Always handle exceptions in a global `AllExceptionsFilter` (`@Catch()`).
- Never catch exceptions in controllers unless converting to a specific HTTP response shape.

## Configuration

- Always inject `ConfigService` for environment variables. Never read `process.env` in services, controllers, or repositories.
- Always validate config with `@nestjs/config` + Joi or `class-validator` in a `ConfigModule.forRoot({ validate })` block.

```typescript
constructor(private readonly config: ConfigService) {}

get jwtSecret(): string {
  return this.config.getOrThrow<string>('JWT_SECRET');
}
```

## Repositories

- Always use `@InjectRepository(Entity)` with typed `Repository<Entity>`.
- Always use QueryBuilder or `find` options with parameterized values. Never concatenate user input into SQL.
- Always paginate list queries when the result set can exceed 100 rows.

```typescript
async findByProject(
  projectId: number,
  organizationId: number,
  page: number,
  size: number,
): Promise<[TaskEntity[], number]> {
  return this.taskRepo.findAndCount({
    where: { projectId, organizationId },
    skip: page * size,
    take: size,
    order: { createdAt: 'DESC' },
  });
}
```
