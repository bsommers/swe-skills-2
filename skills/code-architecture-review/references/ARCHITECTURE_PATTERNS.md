# Architecture Review Reference Patterns & Code Smells

A reference guide for AI agents conducting structural code and architecture reviews.

---

## 1. Core Architectural Paradigms

### A. Layered (N-Tier) Architecture
- **Structure**: Presentation $\rightarrow$ Application / Service $\rightarrow$ Domain $\rightarrow$ Persistence / Database.
- **Rule**: Dependencies only point downwards.
- **Common Violations**: Presentation layer accessing the database directly (skipping domain/service layer); database entities returned directly to the UI/client.

### B. Hexagonal / Ports & Adapters / Clean Architecture
- **Structure**: Domain logic is at the core, completely decoupled from frameworks, databases, and UI.
- **Ports**: Interfaces defining what the domain needs (driving/driven).
- **Adapters**: Concrete implementations (PostgreSQL repo, Stripe payment adapter, Express controller).
- **Rule**: Dependencies point strictly **inward** toward the domain.

### C. Modular Monolith
- **Structure**: Single deployable codebase divided into strictly isolated domain modules.
- **Rule**: Modules communicate only via explicit public interfaces / facade APIs or in-process event buses. No module may directly import another module's internal classes or database tables.

### D. Event-Driven / Pub-Sub
- **Structure**: Producers emit domain events; consumers handle them asynchronously.
- **Rule**: Producers must not assume consumer presence or execution timing. Events should be immutable domain facts.

---

## 2. Common Architectural Smells & Antipatterns

| Code / Architecture Smell | Description | Remediation |
| :--- | :--- | :--- |
| **God Object / Blob** | A single class/module accumulating hundreds or thousands of lines handling disparate concerns. | Extract responsibilities into dedicated domain services or command handlers using SRP. |
| **Circular Dependency** | Module A imports Module B, which directly or indirectly imports Module A. | Introduce a third abstraction layer or utilize the Dependency Inversion Principle (DIP). |
| **Leaky Abstraction** | Internal implementation details (e.g., SQL queries, HTTP status codes, specific library exceptions) bubble up to unrelated layers. | Wrap third-party and database types in domain-specific DTOs and domain error types. |
| **Shotgun Surgery** | A single change requires small modifications across a vast number of disparate files. | Co-locate related logic and enforce high intra-module cohesion. |
| **Feature Envy** | A method in Module A makes continuous calls to get data and manipulate methods inside Module B. | Move the method into Module B or encapsulate the behavior within Module B. |
| **Primitive Obsession** | Using basic strings and integers everywhere instead of domain value objects (e.g. `string` for `EmailAddress`, `UserId`, `Money`). | Introduce value objects with domain validation on instantiation. |
| **Lava Layer / Dead Architecture** | Half-migrated architectures where three different ORMs or API patterns coexist without completion. | Catalog legacy paths in the improvement plan and define retirement milestones. |

---

## 3. Dependency Inversion Transformation Pattern

### ❌ Problem: Concrete Coupling
```typescript
// orderService.ts directly instantiates concrete database & email client
import { PostgresUserRepository } from "./postgres";
import { SendGridEmailClient } from "./sendgrid";

export class OrderService {
  private userRepo = new PostgresUserRepository();
  private emailClient = new SendGridEmailClient();

  async processOrder(order: Order) {
    const user = await this.userRepo.findById(order.userId);
    await this.emailClient.send(user.email, "Order confirmed");
  }
}
```

### ✅ Solution: Interface Segregation & Dependency Inversion
```typescript
// domain/ports.ts
export interface UserRepository {
  findById(id: string): Promise<User | null>;
}

export interface NotificationService {
  notifyUser(email: string, message: string): Promise<void>;
}

// domain/orderService.ts
export class OrderService {
  constructor(
    private readonly userRepo: UserRepository,
    private readonly notifier: NotificationService
  ) {}

  async processOrder(order: Order) {
    const user = await this.userRepo.findById(order.userId);
    if (!user) throw new UserNotFoundError(order.userId);
    await this.notifier.notifyUser(user.email, "Order confirmed");
  }
}
```
