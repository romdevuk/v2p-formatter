# AC Matrix – Prompts Control (within “ACs Missing”)

## Goal
Add a “Prompt” control beneath the existing “ACs Missing” section on `/v2p-formatter/ac-matrix`. Users can pick from predefined prompts, add new ones, delete existing ones, and see/insert a placeholder (`{{draft_text}}`) in prompt text.

## Placement (vertical stack)
```
ACs Missing
[existing missing ACs textarea]
[Copy to Clipboard button]

Prompts
[Select Prompt ▼]  [Add Prompt]  [Delete Prompt]
[Prompt Textarea]
[Tip: You can use the placeholder {{draft_text}} inside the prompt text.]
```

## Components & Behavior

### Select Prompt (dropdown)
- Default option: “Select a prompt…”
- Lists all saved prompts by name.
- On change: loads the prompt text into the Prompt Textarea.
- If no prompt selected: textarea is empty/disabled; Delete is disabled.

### Add Prompt (button)
- Opens a small inline form (or modal, implementer’s choice):
  - **Prompt Name** (text input)
  - **Prompt Body** (multiline textarea)
  - Guidance: “You can include {{draft_text}} as a placeholder.”
- Actions: **Save** (add to list, select it, show in textarea), **Cancel** (close form).
- Validation: require name and body; block duplicates or confirm overwrite.

### Delete Prompt (button)
- Enabled only when a prompt is selected.
- Confirmation: “Delete prompt ‘<name>’?” Yes/No.
- On confirm: removes from dropdown; clears textarea and selection.

### Prompt Textarea
- Shows the body of the selected prompt.
- Readonly by default to avoid accidental edits (optional “Edit” toggle if desired; otherwise editing happens only via Add flow).
- Supports placeholder: `{{draft_text}}`.

### Placeholder Tip
- Small muted text below the textarea:
  - “You can use placeholder: {{draft_text}}”
  - Clarify it will be replaced with the current draft’s text snippet.

## States
- **No prompt selected**: dropdown at default, textarea empty/disabled, Delete disabled.
- **Prompt selected**: textarea filled, Delete enabled.
- **Adding prompt**: inline form visible with Save/Cancel.
- **Deleting prompt**: confirmation dialog.

## Styling (match existing dark theme)
- Buttons: use existing secondary/danger styles.
- Dropdown: match existing selects.
- Textarea: match ACs Missing textarea (dark bg, light text).
- Tip text: small, muted (#999).

## Validation & Messaging
- Add: name + body required; duplicate names blocked or require confirmation.
- Delete: confirmation required.
- If no prompt selected and Delete clicked: show “Select a prompt to delete.”

## Optional Enhancements (not required in first pass)
- Persist prompts per user/session (localStorage or backend).
- Remember last selected prompt.
- Inline “Edit” mode for prompt text (with Save/Cancel).
- Search filter for prompt list if it grows large.





