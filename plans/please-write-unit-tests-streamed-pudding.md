## Unit Test Development Plan

### Scope
Current pending files: AudioRecorder.tsx, ChatInputArea.tsx, ChatMessage.tsx, Chat.tsx

### Testing Framework
- Vitest
- React Testing Library

### Test Coverage

**AudioRecorder.tsx**
- [ ] Initial recording button state
- [ ] Recording start/stop functionality
- [ ] Transcription display
- [ ] Error handling (mic permission, STT failure)

**ChatInputArea.tsx**
- [ ] Input value binding
- [ ] Send button enable/disable
- [ ] Loading state during send

**ChatMessage.tsx**
- [ ] User/assistant role styling
- [ ] Content rendering

**Chat.tsx** (Integration)
- [ ] Full user message flow
- [ ] AI response handling
- [ ] Audio component integration
- [ ] Error states (API fail, mic denied)
- [ ] Scroll behavior

### Implementation Approach
1. Create test files alongside components using `*_test.tsx` naming
2. Mock STT and LLM APIs using Jest mocks
3. Test both happy paths and error scenarios
4. Ensure accessibility attributes (aria-label)

### Verification Steps
- Run tests with `make client/test`
- Check test coverage report
- Manual spot-check of test cases