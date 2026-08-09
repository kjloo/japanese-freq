import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { vi } from "vitest";
import axios from "axios";
import Chat from "../Chat";

// Mock scrollIntoView
beforeAll(() => {
  window.HTMLElement.prototype.scrollIntoView = vi.fn();
});

// Mock axios
vi.mock("axios", () => ({
  default: {
    post: vi.fn(),
    isAxiosError: vi.fn((error) => error?.isAxiosError ?? false),
  },
}));

describe("Chat", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  test("renders header", () => {
    render(<Chat />);
    expect(screen.getByText("Chat with AI")).toBeInTheDocument();
  });

  test("renders empty state when no messages", () => {
    render(<Chat />);
    expect(screen.getByText(/Start a conversation!/)).toBeInTheDocument();
  });

  test("allows text input", () => {
    render(<Chat />);
    expect(
      screen.getByPlaceholderText("Type your message..."),
    ).toBeInTheDocument();
  });

  test("handles send button click", async () => {
    const mockPost = vi.spyOn(axios, "post").mockResolvedValue({
      data: { response: "Hello!" },
    });

    render(<Chat />);

    fireEvent.change(screen.getByPlaceholderText("Type your message..."), {
      target: { value: "Hello" },
    });
    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(mockPost).toHaveBeenCalledWith("/api/llm/generate", {
        prompt: "Hello",
        system_prompt: "You are a helpful assistant.",
        max_tokens: 1000,
      });
    });
  });

  test("displays user message after send", async () => {
    vi.spyOn(axios, "post").mockResolvedValue({
      data: { response: "Hi there!" },
    });

    render(<Chat />);

    fireEvent.change(screen.getByPlaceholderText("Type your message..."), {
      target: { value: "Hello" },
    });
    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(screen.getByText("Hello")).toBeInTheDocument();
    });
  });

  test("shows loading state during API call", async () => {
    vi.spyOn(axios, "post").mockImplementation(
      () =>
        new Promise((resolve) =>
          setTimeout(() => resolve({ data: { response: "OK" } }), 100),
        ),
    );

    render(<Chat />);

    fireEvent.change(screen.getByPlaceholderText("Type your message..."), {
      target: { value: "Test" },
    });
    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(screen.getByText("...")).toBeInTheDocument();
    });
  });

  test("handles Enter key press to send", async () => {
    const mockPost = vi.spyOn(axios, "post").mockResolvedValue({
      data: { response: "Got it!" },
    });

    render(<Chat />);

    fireEvent.change(screen.getByPlaceholderText("Type your message..."), {
      target: { value: "Hello" },
    });
    fireEvent.keyDown(screen.getByPlaceholderText("Type your message..."), {
      key: "Enter",
    });

    await waitFor(() => {
      expect(mockPost).toHaveBeenCalled();
    });
  });

  test("handles API errors", async () => {
    vi.spyOn(axios, "post").mockRejectedValue(new Error("Network error"));

    render(<Chat />);

    fireEvent.change(screen.getByPlaceholderText("Type your message..."), {
      target: { value: "Test" },
    });
    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(screen.getByText(/Error:/)).toBeInTheDocument();
    });
  });

  test("renders audio recorder component", () => {
    render(<Chat />);
    // Use aria-label to locate the button
    expect(screen.getByLabelText(/Start recording/i)).toBeInTheDocument();
  });
});
