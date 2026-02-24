const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

interface LoginCredentials {
  username: string;
  password: string;
}

interface User {
  id: number;
  username: string;
  email: string;
}

export interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  user?: User;
}

interface TaskInput {
  title: string;
  description?: string;
}

class ApiClient {
  private token: string | null = null;

  constructor() {
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('auth_token');
    }
  }

  setToken(token: string | null) {
    this.token = token;
    if (typeof window !== 'undefined') {
      if (token) {
        localStorage.setItem('auth_token', token);
      } else {
        localStorage.removeItem('auth_token');
      }
    }
  }

  getToken(): string | null {
    return this.token;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      (headers as Record<string, string>)['Authorization'] = `Token ${this.token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Request failed' }));
      throw new Error(error.error || error.detail || 'Request failed');
    }

    // Handle empty responses (like DELETE)
    const text = await response.text();
    return text ? JSON.parse(text) : (null as T);
  }

  // Auth endpoints
  async login(credentials: LoginCredentials): Promise<User> {
    const user = await this.request<User>('/login/', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
    return user;
  }

  // Task endpoints
  async getTasks(): Promise<Task[]> {
    const response = await this.request<{ results: Task[] } | Task[]>('/tasks/');
    // Handle paginated and non-paginated responses
    return Array.isArray(response) ? response : response.results;
  }

  async getTask(id: number): Promise<Task> {
    return this.request<Task>(`/tasks/${id}/`);
  }

  async createTask(task: TaskInput): Promise<Task> {
    return this.request<Task>('/tasks/', {
      method: 'POST',
      body: JSON.stringify(task),
    });
  }

  async updateTask(id: number, task: Partial<TaskInput>): Promise<Task> {
    return this.request<Task>(`/tasks/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(task),
    });
  }

  async deleteTask(id: number): Promise<void> {
    await this.request<void>(`/tasks/${id}/`, {
      method: 'DELETE',
    });
  }

  async toggleTask(id: number): Promise<Task> {
    return this.request<Task>(`/tasks/${id}/toggle/`, {
      method: 'POST',
    });
  }

  async getCompletedTasks(): Promise<Task[]> {
    const response = await this.request<{ results: Task[] } | Task[]>('/tasks/completed/');
    return Array.isArray(response) ? response : response.results;
  }

  async getPendingTasks(): Promise<Task[]> {
    const response = await this.request<{ results: Task[] } | Task[]>('/tasks/pending/');
    return Array.isArray(response) ? response : response.results;
  }
}

export const api = new ApiClient();
