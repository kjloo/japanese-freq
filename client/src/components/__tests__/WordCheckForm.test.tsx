import {
  render,
  screen,
  fireEvent,
  waitFor,
  act,
} from "@testing-library/react";
import { vi, Mock } from "vitest";

interface MockSocket {
  on: Mock;
  off: Mock;
  emit: Mock;
}

let mockedSocket: MockSocket;

vi.mock("socket.io-client", () => {
  const on = vi.fn();
  const off = vi.fn();
  const emit = vi.fn();
  mockedSocket = { on, off, emit };
  return { io: vi.fn(() => mockedSocket) };
});
import WordCheckForm from "../WordCheckForm";

// Helper to get the registered callback for a given event
function getCallbackForEvent(
  eventName: string,
): ((data: unknown) => void) | undefined {
  const calls = mockedSocket.on.mock.calls as [
    string,
    (data: unknown) => void,
  ][];
  const call = calls.find((c) => c[0] === eventName);
  return call?.[1];
}

describe("WordCheckForm", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  test("shows waiting message initially", () => {
    render(<WordCheckForm />);
    expect(screen.getByText(/waiting for a word/i)).toBeInTheDocument();
  });

  test("renders word data when socket emits", async () => {
    const mockData = {
      word: "test",
      frequency: 42,
      definition: {
        definition: "a trial",
        kanji: "試",
        hiragana: "し",
        romaji: "shi",
      },
    };

    render(<WordCheckForm />);
    const callback = getCallbackForEvent("word_check");
    expect(callback).toBeDefined();

    // Simulate receiving data via socket
    await act(async () => {
      callback?.(mockData);
    });

    await waitFor(() => {
      expect(screen.getByText("test")).toBeInTheDocument();
      expect(screen.getByText("42")).toBeInTheDocument();
    });
  });

  test("clicking Yes/No emits response", async () => {
    const mockData = {
      word: "sample",
      frequency: 10,
      definition: {
        definition: "example",
        kanji: "例",
        hiragana: "れい",
        romaji: "rei",
      },
    };

    render(<WordCheckForm />);
    const callback = getCallbackForEvent("word_check");
    expect(callback).toBeDefined();
    await act(async () => {
      callback?.(mockData);
    });

    await waitFor(() => screen.getByText(/word:/i));
    const yesBtn = screen.getByText("Yes");
    fireEvent.click(yesBtn);
    expect(mockedSocket.emit).toHaveBeenCalledWith("word_response", {
      word: "sample",
      answer: true,
    });
  });
});
