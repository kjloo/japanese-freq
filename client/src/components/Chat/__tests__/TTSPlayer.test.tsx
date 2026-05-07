import { render } from "@testing-library/react";
import { vi, expect, test, beforeEach, afterEach } from "vitest";
import { TTSPlayer } from "../TTSPlayer";

// Mock fetch to return a dummy audio blob
const mockBlob = new Blob(["dummy"], { type: "audio/mp3" });

// Create typed mocks outside so we can reference them in assertions
let fetchMock: ReturnType<typeof vi.fn>;
let audioConstructorMock: ReturnType<typeof vi.fn>;
let playMock: ReturnType<typeof vi.fn>;

beforeEach(() => {
  // Create fetch mock with proper typing
  fetchMock = vi.fn().mockResolvedValue({
    ok: true,
    blob: () => Promise.resolve(mockBlob),
  } as unknown as Response);
  vi.stubGlobal("fetch", fetchMock);

  // Mock URL.createObjectURL and revokeObjectURL (missing in jsdom)
  vi.stubGlobal("URL", {
    createObjectURL: vi.fn(() => "blob:mock-url"),
    revokeObjectURL: vi.fn(),
  });

  // Create play mock
  playMock = vi.fn().mockResolvedValue(undefined);

  // Mock Audio as a vi.fn constructor
  audioConstructorMock = vi.fn(function (
    this: Record<string, unknown>,
    src: string,
  ) {
    this.src = src;
    this.play = playMock;
    this.onended = null;
  });
  vi.stubGlobal("Audio", audioConstructorMock);
});

afterEach(() => {
  vi.restoreAllMocks();
});

test("TTSPlayer fetches audio and plays it", async () => {
  render(<TTSPlayer text="こんにちは" />);

  // Wait for fetch to be called with correct args
  await vi.waitFor(() => {
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/speech/tts",
      expect.objectContaining({
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: "こんにちは", language: "Japanese" }),
      }),
    );
  });

  // Wait for Audio constructor to be called and play() to be invoked
  await vi.waitFor(() => {
    expect(audioConstructorMock).toHaveBeenCalledTimes(1);
    // Verify play was called on the instance
    expect(playMock).toHaveBeenCalledTimes(1);
  });
});
