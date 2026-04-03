type StatusMessageProps = {
  tone: 'error' | 'info' | 'success'
  message: string
}

export function StatusMessage({ tone, message }: StatusMessageProps) {
  return <p className={`status-message status-message--${tone}`}>{message}</p>
}
