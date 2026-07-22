import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

// =========================================================================
// HANDS-ON 10: Task 3 - Global Error Boundary Component
// =========================================================================
export default class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    // Update state so the next render will show the fallback UI.
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('[Global ErrorBoundary Caught Unhandled Error]:', error, errorInfo);
  }

  private handleReset = () => {
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div style={styles.container}>
          <div style={styles.card}>
            <div style={styles.icon}>⚠️</div>
            <h2 style={styles.heading}>Something Went Wrong</h2>
            <p style={styles.message}>
              A runtime component error occurred. Our global Error Boundary caught the issue gracefully.
            </p>

            {this.state.error && (
              <pre style={styles.errorBox}>
                <code>{this.state.error.toString()}</code>
              </pre>
            )}

            <button style={styles.button} onClick={this.handleReset}>
              🔄 Reload Application
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    backgroundColor: '#f8fafc',
    padding: '20px',
  },
  card: {
    backgroundColor: '#ffffff',
    padding: '30px',
    borderRadius: '12px',
    boxShadow: '0 10px 25px rgba(0,0,0,0.1)',
    maxWidth: '550px',
    textAlign: 'center',
    border: '2px solid #fee2e2',
  },
  icon: {
    fontSize: '48px',
    marginBottom: '10px',
  },
  heading: {
    color: '#991b1b',
    fontSize: '24px',
    marginBottom: '10px',
  },
  message: {
    color: '#4b5563',
    marginBottom: '20px',
    lineHeight: '1.5',
  },
  errorBox: {
    backgroundColor: '#fef2f2',
    color: '#b91c1c',
    padding: '12px',
    borderRadius: '6px',
    textAlign: 'left',
    fontSize: '13px',
    overflowX: 'auto',
    marginBottom: '20px',
    border: '1px solid #fca5a5',
  },
  button: {
    backgroundColor: '#1d4ed8',
    color: '#ffffff',
    border: 'none',
    padding: '12px 24px',
    borderRadius: '6px',
    fontSize: '15px',
    fontWeight: 'bold',
    cursor: 'pointer',
  },
};
