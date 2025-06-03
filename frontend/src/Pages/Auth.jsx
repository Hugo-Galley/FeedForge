import "../styles/authpage.css"
import logo from "../assets/logo-2.png"
import RegisterForm from "../components/RegisterForm"
import LoginForm from "../components/LoginForm";
import { useState } from "react";
export default function AuthPage({onAuthSuccess}){
const [isLoginView, setIsLoginView] = useState(true);
const [registrationSuccess, setRegistrationSuccess] = useState(false);

    const handleLoginSuccess = (userData) => {
    onAuthSuccess(userData);
  };

  const handleRegisterSuccess = () => {
    setRegistrationSuccess(true);
  };

    return(
        <div className="container">
            <div className="decoration-page">
                <div className="decoration-container">
                    <div className="logo">
                        <img src={logo} alt="logo" />
                        <p>FeedForge</p>
                    </div>
                    <div className="description">
                        <h1>Commmencer avec nous</h1>
                        <p>Completer toutes les étapes pour finaliser l'inscription et la création de votre profil</p>
                    </div>
                    <div className="cta-container">
                        <ul>
                            <li className="cta" id="numberOne">
                                <p id="number-cta">1</p>
                                <p>Crée votre compte</p>
                            </li>
                            <li className="cta">
                                <p id="number-cta">2</p>
                                <p>Completer votre profil</p>
                            </li>
                            <li className="cta">
                                <p id="number-cta">3</p>
                                <p>Crée votre flux Rss personalisé</p>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
                 {registrationSuccess && isLoginView && (
        <div className="success-message">
          Inscription réussie ! Vous pouvez maintenant vous connecter.
        </div>
      )}
            <div className="form">
                   {isLoginView ? (
        <LoginForm 
          onSwitchToRegister={() => {
            setIsLoginView(false);
            setRegistrationSuccess(false);
          }}
          loginSucces={handleLoginSuccess}
        />
      ) : (
        <RegisterForm 
          onSwitchToLogin={() => setIsLoginView(true)}
          onRegisterSuccess={handleRegisterSuccess}
        />
      )}
            </div>
        </div>
    )
}