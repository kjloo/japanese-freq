import { render, screen } from "@testing-library/react";
import ChatMessage from "../ChatMessage";

describe("ChatMessage", () => {
  test("renders user message content", () => {
    render(<ChatMessage id="1" role="user" content="Hello" />);
    expect(screen.getByText("Hello")).toBeInTheDocument();
  });

  test("renders assistant message content", () => {
    render(<ChatMessage id="2" role="assistant" content="Hi there" />);
    expect(screen.getByText("Hi there")).toBeInTheDocument();
  });

  test("applies user role class", () => {
    const { container } = render(
      <ChatMessage id="3" role="user" content="test" />,
    );
    const outerDiv = container.firstChild as HTMLElement;
    expect(outerDiv?.className).toMatch(/user/);
  });

  test("applies assistant role class", () => {
    const { container } = render(
      <ChatMessage id="4" role="assistant" content="test" />,
    );
    const outerDiv = container.firstChild as HTMLElement;
    expect(outerDiv?.className).toMatch(/assistant/);
  });
});
