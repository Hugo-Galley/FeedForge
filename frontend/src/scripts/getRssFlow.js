export default async function getRssFlow(){
    const response = await fetch("http://localhost:8000/getRssFlow",{
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
        
    if (!response.ok){
        console.error("Erreur lors de récuperation des flux Rss")
    }
    const data = await response.json()
    const colors = ["magenta", "red", "volcano", "orange", "gold", "lime", "green", "cyan", "blue", "geekblue", "purple"];
    const rssFlows = data["rssFlows"].map(flow => ({
        ...flow,
        color: colors[Math.floor(Math.random() * colors.length)]
    }))
    return rssFlows
}