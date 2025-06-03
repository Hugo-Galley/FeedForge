import "../styles/form.css"
import { useState } from "react";
export default function LoginForm({ onSwitchToRegister, loginSucces }){
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [error, setError] = useState('')

    async function VerifySucces(e){
        e.preventDefault()
        console.log(`On verifie le succées pour ${email} et ${password}`)
        // const result = await LoginUser(email, password, e)
        // if (result === false){
        //     setError("Nom d'utilisateur ou mot de passe incorect") 
        // }
        // else{
        //     loginSucces(result)
        // }

    }

    return (
        <div className="container-form">
            <div className="head-description">
                <h1>Connecter vous</h1>
                <p>Entrer vos informations pour vous connecter à votre compte</p>
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
            <form onSubmit={VerifySucces} className="registerForm">
                {error && <div className='error-message'>{error}</div>}
                    <label htmlFor="email">Entrer votre email</label>
                    <input type="email" id="email" placeholder="johndoe@mail.com" onChange={(e) => setEmail(e.target.value)}/>
                    <label htmlFor="password">Entrer votre mot de passe</label>
                    <input type="password" id="password" placeholder="Entrer votre mot de passe" onChange={(e) => setPassword(e.target.value)}/>
                    <button className="signinButton">S'inscrire</button>
            </form>
                <button onClick={onSwitchToRegister} className="switch-button"><p>Pas de compte? S'inscrire</p></button>
        </div>
    )
}