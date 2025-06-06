import { useEffect, useState } from 'react';
import '../styles/CreatRssFlowPage.css'
import { PlusOutlined,CloseOutlined, ArrowRightOutlined } from '@ant-design/icons';
import {Badge , Space, Select, Input, Tag, Button } from 'antd';

export default function CreateRssFlow(){
    const [selectedFlow,setSelectedFlow] = useState([])
    const [initialFlow,setInitialFlow] = useState([])
    const [FilterinitialFlow,setFiltrerInitialFlow] = useState([])
    const [selectedLanguages, setSelectedLanguages] = useState(['Français'])
    const [selectedCategories, setSelectedCategories] = useState(['Presse'])

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

    const options = [
      {
        label: 'Français',
        value: 'Français',
        emoji: '🇫🇷',
        desc: 'Français',
      },
      {
        label: 'Anglais',
        value: 'Anglais',
        emoji: '🇬🇧',
        desc: 'Anglais (English)',
      },
      {
        label: 'Espagnol',
        value: 'Espagnol',
        emoji: '🇪🇸',
        desc: 'Espagnol (Español)',
      },
      {
        label: 'Chinois',
        value: 'Chinois',
        emoji: '🇨🇳',
        desc: 'Chinois (中文)',
      },
    ];
    const categoryOptions = [
        {
            label: 'Presse',
            value: 'Presse',
            emoji: '📰',
            desc: 'Presse (Journaux, Magazines, etc.)',
        },
        {
            label: 'Youtube',
            value: 'Youtube',
            emoji: '📺',
            desc: 'Youtube (Chaînes vidéo)',
        },
        {
            label: 'Medium',
            value: 'Medium',
            emoji: '✍️',
            desc: 'Medium (Blogs, Articles)',
        },
    ];
    function applyFilters(){
        let filterFlows = initialFlow;

        if (selectedLanguages.length > 0){
            filterFlows = filterFlows.filter(f => selectedLanguages.includes(f.language))
        }
        if (selectedCategories.length > 0){
            filterFlows = filterFlows.filter(f => selectedCategories.includes(f.category))
        }
        filterFlows = filterFlows.filter(f => !selectedFlow.some(selected => selected.name === f.name))

        setFiltrerInitialFlow(filterFlows)
    }

    function moveFlow(flow, type) {
        if (type === "add") {
            if (!selectedFlow.some(f => f.name === flow.name)) {
                setSelectedFlow([...selectedFlow, flow]);
                setTimeout(() => applyFilters(), 0);
            }
        } else {
            setSelectedFlow(selectedFlow.filter(f => f.name !== flow.name))
            setTimeout(() => applyFilters(), 0);
        }
    }

    useEffect(() =>{
        if (initialFlow.length > 0) {
            applyFilters()
        }
    })

    useEffect(()=>{
        setInitialFlow(tags)
        setFiltrerInitialFlow(tags)
    },[])

        function filterFlowByLanguage(languageList) {
        setSelectedLanguages(languageList);
    }
    
    function filterFlowByCategory(categoryList) {
        setSelectedCategories(categoryList);
    }

    return(
        <div>
            <div className='main-div'>
                <div className="header">
                    <h2 className="yourName">Freaks</h2>
                    <p className="description">Création de votre Flow personalisé</p>
                </div>
                <div className="searchBar-container">
                    <Input placeholder="input search text" variant='borderless' className="searchBar"/>
                    <div className='language-filter'>
                        <Select
                        mode='multiple'
                        style={{width:'100%'}}
                        placeholder="Langues"
                        defaultValue={['Français']}
                        onChange={filterFlowByLanguage}
                        options={options}
                        optionRender={(option) => (
                            <Space>
                                <span role='img' aria-label={option.data.label}>
                                    {option.data.emoji}
                                </span>
                                {option.data.desc}
                            </Space>
                        )}
                        />
                    </div>

                    <div className='category-filter'>
                    <Select
                        mode='multiple'
                        style={{width:'100%'}}
                        placeholder="Categories"
                        defaultValue={['Presse']}
                        onChange={filterFlowByCategory}
                        options={categoryOptions}
                        optionRender={(option) => (
                            <Space>
                                <span role='img' aria-label={option.data.label}>
                                    {option.data.emoji}
                                </span>
                                {option.data.desc}
                            </Space>
                        )}
                        />
                    </div>


                </div>
                <div className="badge-ribbon-container">
                <Badge.Ribbon text="RssFlow">
                    <div className="recommandedRssFlow">
                    {FilterinitialFlow.map((tag, key) => (
                        <div key={key}>
                        <Tag color={tag.color} className='tag' onClick={() => moveFlow(tag,"add")} >
                            <img src={tag.logoUrl} alt={tag.name} className="tag-logo"/>
                            <span className="tag-name">{tag.name}</span>
                            <PlusOutlined />
                        </Tag>
                        </div>
                    ))}           
                    </div>
                </Badge.Ribbon>
                </div>
                
                <div className="badge-ribbon-container">
                <Badge.Ribbon text="Vos Flows" color='pink'>
                    <div className="recommandedRssFlow">
                    {selectedFlow.map((tag, key) => (
                        <div key={key}>
                        <Tag color={tag.color} className='tag' onClick={() => moveFlow(tag,"remove")} >
                            <img src={tag.logoUrl} alt={tag.name} className="tag-logo"/>
                            <span className="tag-name">{tag.name}</span>
                            <CloseOutlined />
                        </Tag>
                        </div>
                    ))}           
                    </div>
                </Badge.Ribbon>
                </div>
            </div>
            <div className='nextButton'>
            <Button type="primary"  icon={<ArrowRightOutlined />} iconPosition='end' size='large' >
                Suivant
            </Button>
            </div>
        </div>
    )
}