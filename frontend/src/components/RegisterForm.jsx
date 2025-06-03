import "../styles/form.css"
import { useState } from "react";
export default function RegisterForm({ onSwitchToLogin, onRegisterSuccess }){
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [error, setError] = useState('')

        async function VerifyRegister(e){
        const [message,result] = await RegisterUser(username,password,email)
        if(result){
            onRegisterSuccess(result)
            onSwitchToLogin()
        }
        else{
            setError(message)
        }

    }

    return (
        <div className="container-form">
            <div className="head-description">
                <h1>Crée votre compte</h1>
                <p>Entrer vos informations pour crée votre compte</p>
            </div>
            <div className="alternative-connexion">
                <div className="SignInWithGoogle">
                    Sign in With Google
                </div>
                <div className="SignInWithApple">
                    Sign in With Apple
                </div>
            </div>
                <div className="separator">
                    <div className="line"></div>
                    <span>OR</span>
                    <div className="line"></div>
                </div>
            <form onSubmit={(e) => VerifyRegister(e)} className="registerForm">
                {error && <div className='error-message'>{error}</div>}
                    <label htmlFor="username">Username</label>
                    <input type="text" id="username" placeholder="Doe" onChange={(e) => setUsername(e.target.value)}/>
                    <label htmlFor="email">Entrer votre email</label>
                    <input type="email" id="email" placeholder="johndoe@mail.com" onChange={(e) => setEmail(e.target.value)}/>
                    <label htmlFor="password">Entrer votre mot de passe</label>
                    <input type="password" id="password" placeholder="Entrer votre mot de passe" onChange={(e) => setPassword(e.target.value)}/>
                    <button className="signinButton">S'inscrire</button>
            </form>
                <button onClick={onSwitchToLogin} className="switch-button"><p>Déja un compte ? Se connecter</p></button>
        </div>
    )
}