import React, { useState } from 'react';
import { User, Lock, ArrowRight, AlertCircle } from 'lucide-react';
import users from './users.json'; // Importing users for mock authentication
import LogoIcon from './LogoIcon';

function Login({ onLogin }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleLogin = (e) => {
        e.preventDefault();
        setError('');

        if (!username || !password) {
            setError('Please enter both username and password');
            return;
        }

        const user = users.find(
            (u) => u.username === username && u.password === password
        );

        if (user) {
            onLogin(user);
        } else {
            setError('Invalid username or password');
        }
    };

    return (
        <div
            style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100vh',
                width: '100%',
                background: 'var(--bg-primary)',
            }}
        >
            <div
                className="glass-card"
                style={{
                    width: '100%',
                    maxWidth: '400px',
                    padding: '40px',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '24px',
                }}
            >
                <div style={{ textAlign: 'center' }}>
                    <div
                        style={{
                            width: '64px',
                            height: '64px',
                            background: 'rgba(124, 77, 255, 0.1)',
                            borderRadius: '50%',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            margin: '0 auto 16px',
                        }}
                    >
                        <Lock size={32} color="var(--accent-color)" />
                        {/* <LogoIcon width={256} height={256} color="var(--accent-color)" /> */}
                    </div>
                    <h1 style={{ margin: 0, fontSize: '24px', fontWeight: 600 }}>Welcome</h1>
                    <p style={{ color: 'var(--text-secondary)', marginTop: '8px' }}>
                        Please sign in to continue
                    </p>
                </div>

                {error && (
                    <div
                        style={{
                            background: 'rgba(255, 82, 82, 0.1)',
                            border: '1px solid #ff5252',
                            color: '#ff5252',
                            padding: '12px',
                            borderRadius: '8px',
                            fontSize: '14px',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                        }}
                    >
                        <AlertCircle size={16} />
                        {error}
                    </div>
                )}

                <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <div>
                        <label
                            style={{
                                display: 'block',
                                marginBottom: '8px',
                                fontSize: '14px',
                                fontWeight: 500,
                                color: 'var(--text-secondary)',
                            }}
                        >
                            Username
                        </label>
                        <div style={{ position: 'relative' }}>
                            <User
                                size={18}
                                style={{
                                    position: 'absolute',
                                    left: '12px',
                                    top: '50%',
                                    transform: 'translateY(-50%)',
                                    color: 'var(--text-secondary)',
                                }}
                            />
                            <input
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                className="chat-input"
                                placeholder="Enter your username"
                                style={{ paddingLeft: '40px' }}
                            />
                        </div>
                    </div>

                    <div>
                        <label
                            style={{
                                display: 'block',
                                marginBottom: '8px',
                                fontSize: '14px',
                                fontWeight: 500,
                                color: 'var(--text-secondary)',
                            }}
                        >
                            Password
                        </label>
                        <div style={{ position: 'relative' }}>
                            <Lock
                                size={18}
                                style={{
                                    position: 'absolute',
                                    left: '12px',
                                    top: '50%',
                                    transform: 'translateY(-50%)',
                                    color: 'var(--text-secondary)',
                                }}
                            />
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="chat-input"
                                placeholder="Enter your password"
                                style={{ paddingLeft: '40px' }}
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        className="btn-primary"
                        style={{
                            marginTop: '8px',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            gap: '8px',
                            width: '100%',
                            padding: '12px',
                        }}
                    >
                        Sign In <ArrowRight size={18} />
                    </button>
                </form>
            </div>
        </div>
    );
}

export default Login;
