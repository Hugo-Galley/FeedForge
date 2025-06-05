import { useEffect, useState } from 'react';
import '../styles/CreatRssFlowPage.css'
import { PlusOutlined, DownOutlined,CloseOutlined } from '@ant-design/icons';
import { Dropdown, Space, Typography, Checkbox, Input, Tag, Flex } from 'antd';

export default function CreateRssFlow(){
    const [selectedLanguages,setSelectedLanguages] = useState(["1"])
    const [selectedCategory,setSelectedCategories] = useState(["1"])
    const [selectedFlow,setSelectedFlow] = useState([])
    const [initialFlow,setInitialFlow] = useState([])

    const langues = [
        {
            key: "Français",
            label: (
                <Checkbox
                    checked={selectedLanguages.includes('Français')}
                    onChange={(e) => handleFilterChange('Français', e.target.checked, "langues")}
                >
                    Français
                </Checkbox>
            )
        },
        {
            key: "Anglais",
            label: (
                <Checkbox
                    checked={selectedLanguages.includes('Anglais')}
                    onChange={(e) => handleFilterChange('Anglais', e.target.checked, "langues")}
                >
                    Anglais
                </Checkbox>
            )
        },
        {
            key: "Espagnol",
            label: (
                <Checkbox
                    checked={selectedLanguages.includes('Espagnol')}
                    onChange={(e) => handleFilterChange('Espagnol', e.target.checked, "langues")}
                >
                    Espagnol
                </Checkbox>
            )
        }
    ];
    const category = [
        {
            key: "Presse",
            label: (
                <Checkbox
                    checked={selectedCategory.includes('Presse')}
                    onChange={(e) => handleFilterChange('Presse', e.target.checked, "categorys")}
                >
                    Presse
                </Checkbox>
            )
        },
        {
            key: "Youtube",
            label: (
                <Checkbox
                    checked={selectedCategory.includes('Youtube')}
                    onChange={(e) => handleFilterChange('Youtube', e.target.checked, "categorys")}
                >
                    Youtube
                </Checkbox>
            )
        },
        {
            key: "Medium",
            label: (
                <Checkbox
                    checked={selectedCategory.includes('Medium')}
                    onChange={(e) => handleFilterChange('Medium', e.target.checked, "categorys")}
                >
                    Medium
                </Checkbox>
            )
        }
    ];

    const colors = ["magenta", "red", "volcano", "orange", "gold", "lime", "green", "cyan", "blue", "geekblue", "purple"];
    
    const tags = [
        {
            "name" : "Le Monde",
            "logoUrl" : "https://logo.clearbit.com/lemonde.fr",
            "color" : colors[Math.floor(Math.random() * colors.length)],
            "language": "Français",
            "category" : "Presse"
        },
        {
            "name" : "Le Figaro",
            "logoUrl" : "https://logo.clearbit.com/lefigaro.fr",
            "color" : colors[Math.floor(Math.random() * colors.length)],
            "language": "Français",
            "category" : "Presse"
        },
        {
            "name" : "Libération",
            "logoUrl" : "https://logo.clearbit.com/liberation.fr",
            "color" : colors[Math.floor(Math.random() * colors.length)],
            "language": "Français",
            "category" : "Presse"
        },
        {
            "name" : "L'Équipe",
            "logoUrl" : "https://logo.clearbit.com/lequipe.fr",
            "color" : colors[Math.floor(Math.random() * colors.length)],
            "language": "Français",
            "category" : "Presse"
        },
        {
            "name" : "France Info",
            "logoUrl" : "https://logo.clearbit.com/francetvinfo.fr",
            "color" : colors[Math.floor(Math.random() * colors.length)],
            "language": "Français",
            "category" : "Presse"
        },
        {
            "name" : "Les Échos",
            "logoUrl" : "https://logo.clearbit.com/lesechos.fr",
            "color" : colors[Math.floor(Math.random() * colors.length)],
            "language": "Français",
            "category" : "Presse"
        },
        {
            "name" : "L'Humanité",
            "logoUrl" : "https://logo.clearbit.com/humanite.fr",
            "color" : colors[Math.floor(Math.random() * colors.length)],
            "language": "Français",
            "category" : "Presse"
        },
        {
            "name" : "20 Minutes",
            "logoUrl" : "https://logo.clearbit.com/20minutes.fr",
            "color" : colors[Math.floor(Math.random() * colors.length)],
            "language": "Français",
            "category" : "Presse"
        },
        {
            "name" : "Ouest France",
            "logoUrl" : "https://logo.clearbit.com/ouest-france.fr",
            "color" : colors[Math.floor(Math.random() * colors.length)],
            "language": "Français",
            "category" : "Presse"
        },
        {
            "name" : "Le Parisien",
            "logoUrl" : "https://logo.clearbit.com/leparisien.fr",
            "color" : colors[Math.floor(Math.random() * colors.length)],
            "language": "Français",
            "category" : "Presse"
        },
        {
            "name": "PewDiePie",
            "logoUrl": "https://logo.clearbit.com/youtube.com",
            "color": colors[Math.floor(Math.random() * colors.length)],
            "language": "Anglais",
            "category": "Youtube"
        }
    ]
    function handleFilterChange(key, checked, type){
        if (checked){
            if (type === "langues"){
                setSelectedLanguages([...selectedLanguages, key])
            }
            else{
                setSelectedCategories([...selectedCategory, key])
            }
            
        }
        else{
            if (type === "langues"){
                setSelectedLanguages(selectedLanguages.filter(lang => lang !== key))
            }
            else{
                setSelectedCategories(selectedCategory.filter(cat => cat !== key))
            }

        }
    }

    function moveFlow(flow, type) {
        if (type === "add") {
            if (!selectedFlow.some(f => f.name === flow.name)) {
                setSelectedFlow([...selectedFlow, flow]);
                setInitialFlow(initialFlow.filter(f => f.name !== flow.name));
            }
        } else {
            setInitialFlow([...initialFlow, flow]);
            setSelectedFlow(selectedFlow.filter(f => f.name !== flow.name));
        }
    }

    function filterFlow({key}){
        setInitialFlow(initialFlow.filter(f => f.language === key))
    }
        
    useEffect(()=>{
        setInitialFlow(tags)
    },[])
    return(
        <div>
            <div className="header">
                <h2 className="yourName">Freaks</h2>
                <p className="description">Création de votre Flow personalisé</p>
            </div>
            <div className="searchBar-container">
                <Input placeholder="input search text" variant='borderless' className="searchBar"/>
                <div className='language-filter'>
                    <Dropdown
                    menu={{
                        items : langues,
                        onClick: filterFlow
                    }}
                    trigger={['click']}
                    
                    >
                        <Typography.Link className="custom-dropdown-link">
                            <Space>
                            Langues
                                <DownOutlined/>
                            </Space>
                        </Typography.Link>
                    </Dropdown>
                </div>

                <div className='category-filter'>
                    <Dropdown
                    menu={{items : category}}
                    trigger={['click']}
                    >
                        <Typography.Link className="custom-dropdown-link">
                            <Space>
                            Categories
                                <DownOutlined/>
                            </Space>
                        </Typography.Link>
                    </Dropdown>
                </div>


            </div>
            <h1 className='title-recommanded-rss'>RssFlow</h1>
            <div className="recommandedRssFlow">
                {initialFlow.map((tag,key) => (
                    <div>
                    <Tag key={key} color={tag.color} className='tag' onClick={() => moveFlow(tag,"add")} >
                        <img src={tag.logoUrl} alt={tag.name} className="tag-logo"/>
                        <span className="tag-name">{tag.name}</span>
                        <PlusOutlined />
                    </Tag>
                   
                    </div>
                ))}                
            </div>
            <h1 className='title-recommanded-rss'>Vos flux selectionné</h1>
            <div className="selectionedRssFlow">
                {selectedFlow.map((tag,key) => (
                    <div>
                    <Tag key={key} color={tag.color} className='tag' onClick={() => moveFlow(tag,"remove")}>
                        <img src={tag.logoUrl} alt={tag.name} className="tag-logo"/>
                        <span className="tag-name">{tag.name}</span>
                        <CloseOutlined />
                    </Tag>
                   
                    </div>
                ))}      
            </div>
        </div>
    )
}