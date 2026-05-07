import { render, screen, fireEvent } from "@testing-library/react";
import ChatInputArea from "../Chat/ChatInputArea";

describe("ChatInputArea", () => {
  const handleSend = vi.fn();

  test("renders input field", () => {
    render(
      <ChatInputArea
        input=""
        setInput={vi.fn()}
        handleSend={handleSend}
        isLoading={false}
      />,
    );
    expect(
      screen.getByPlaceholderText("Type your message..."),
    ).toBeInTheDocument();
  });

  test("renders send button", () => {
    render(
      <ChatInputArea
        input=""
        setInput={vi.fn()}
        handleSend={handleSend}
        isLoading={false}
      />,
    );
    expect(screen.getByText("Send")).toBeInTheDocument();
  });

  test("calls setInput on input change", () => {
    const setInput = vi.fn();
    render(
      <ChatInputArea
        input=""
        setInput={setInput}
        handleSend={handleSend}
        isLoading={false}
      />,
    );

    fireEvent.change(screen.getByPlaceholderText("Type your message..."), {
      target: { value: "Hello" },
    });
    expect(setInput).toHaveBeenCalledWith("Hello");
  });

  test("disables send button when input is empty", () => {
    render(
      <ChatInputArea
        input=""
        setInput={vi.fn()}
        handleSend={handleSend}
        isLoading={false}
      />,
    );
    expect(screen.getByText("Send")).toBeDisabled();
  });

  test("disables send button when loading", () => {
    render(
      <ChatInputArea
        input="test"
        setInput={vi.fn()}
        handleSend={handleSend}
        isLoading={true}
      />,
    );
    expect(screen.getByText("...")).toBeInTheDocument();
  });

  test("calls handleSend when send button clicked", () => {
    render(
      <ChatInputArea
        input="test"
        setInput={vi.fn()}
        handleSend={handleSend}
        isLoading={false}
      />,
    );
    fireEvent.click(screen.getByText("Send"));
    expect(handleSend).toHaveBeenCalled();
  });
});
