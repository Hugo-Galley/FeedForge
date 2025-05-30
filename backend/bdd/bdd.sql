CREATE DATABASE `FeedForge`;
USE `FeedForge`;

-- Une table User classique
CREATE TABLE Users (
    userId CHAR(36) NOT NULL PRIMARY KEY,
    username NOT NULL VARCHAR(255),
    email NOT NULL VARCHAR(255),
    passwd NOT NULL TEXT,
    profilPicture NOT NULL TEXT
);

-- une table pour stocker les flux RSS avec les infos (scrapper le site de flux dis dans notion)
CREATE TABLE RssFlowLibrary(
    rssFlowLibraryId NOT NULL CHAR(36) PRIMARY KEY,
    flowName NOT NULL VARCHAR(255),
    flowLink NOT NULL TEXT,
    category NOT NULL VARCHAR(255),
    logo TEXT NOT NULL,
    domains TEXT NOT NULL
);

-- Une table pour stocker les identifiant de chaine youtube associé a leur nom affin d'evité les appel API trop couteux
CREATE TABLE YoutubeChannelId(
    name NOT NULL PRIMARY KEY,
    channelId TEXT NOT NULL
);

-- une table pour stocker les infos lié au flux de la personne (Article vidéo, etc)
CREATE TABLE CustomRssFlow(
    customRssFlowId CHAR(36) NOT NULL PRIMARY KEY,
    articleTitle NOT NULL TEXT,
    articlePublicationDate NOT NULL TEXT,
    articleLink NOT NULL TEXT,
    articleDescription NOT NULL TEXT,
    articleLanguage NOT NULL VARCHAR(30),
    rssFlowLibrairyId NOT NULL CHAR(36),
    userId NOT NULL CHAR(36),
    FOREIGN KEY (rssFlowLibrairyId) REFERENCES RssFlowLibrary(rssFlowLibraryId) ON DELETE CASCADE,
    FOREIGN KEY (userId) REFERENCES Users(userId) ON DELETE CASCADE
);
