import logo from "../assets/logo-2.png"
import '../styles/navbar.css'

export default function NavBar(){
    return(
        <div className="navbar-container">
            <img src={logo} alt="logo" />
            <ul>
                <li>Your Flow</li>
                <li>Customize</li>
                <li>Account</li>
            </ul>
        </div>
    )
}