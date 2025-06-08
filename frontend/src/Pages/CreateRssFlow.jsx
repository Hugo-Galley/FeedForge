import { useEffect, useState } from 'react';
import '../styles/CreatRssFlowPage.css'
import { PlusOutlined,CloseOutlined, ArrowRightOutlined } from '@ant-design/icons';
import {Badge , Space, Select, Input, Tag, Button } from 'antd';
import getRssFlow from '../scripts/getRssFlow';

export default function CreateRssFlow(){
    const [selectedFlow,setSelectedFlow] = useState([])
    const [initialFlow,setInitialFlow] = useState([])
    const [FilterinitialFlow,setFiltrerInitialFlow] = useState([])
    const [selectedCategories, setSelectedCategories] = useState([])

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
        let filterFlows = [...initialFlow]; 
        if (selectedCategories.length > 0){
            filterFlows = filterFlows.filter(f => selectedCategories.includes(f.category))
        }
        filterFlows = filterFlows.filter(f => !selectedFlow.some(selected => selected.flowName === f.flowName))

        setFiltrerInitialFlow(filterFlows)
    }

    function moveFlow(flow, type) {
        if (type === "add") {
            if (!selectedFlow.some(f => f.flowName === flow.flowName)) {
                setSelectedFlow([...selectedFlow, flow]);
            }
        } else {
            setSelectedFlow(selectedFlow.filter(f => f.flowName !== flow.flowName))
            setTimeout(() => applyFilters(), 0);
        }
    }

    useEffect(() => {
        if (initialFlow.length > 0) {
            applyFilters();
        }
    }, [initialFlow, selectedCategories, selectedFlow]);
    useEffect(()=>{
        async function fetchTags() {
            const tags = await getRssFlow();
            setInitialFlow(tags);
            setFiltrerInitialFlow(tags);
        }
        fetchTags();
    },[])

    
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
                        
                    </div>

                    <div className='category-filter'>
                    <Select
                        mode='multiple'
                        style={{width:'100%'}}
                        placeholder="Categories"
                        defaultValue={[]}
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
                            {tag.logo && (
                                <img src={tag.logo} alt={tag.flowName} className="tag-logo"/>
                            )}
                            <span className="tag-name">{tag.flowName}</span>
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
                            {tag.logo && (
                                <img src={tag.logo} alt={tag.flowName} className="tag-logo"/>
                            )}
                            <span className="tag-name">{tag.flowName}</span>
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