CREATE DATABASE IF NOT EXISTS db; USE db; 

CREATE TABLE medicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    crm VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL 
);

CREATE TABLE pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    sexo ENUM('M', 'F') NOT NULL,
    data_nascimento DATE NOT NULL,
    nome_responsavel VARCHAR(100),
    medico_id INT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (medico_id) REFERENCES medicos(id)
);

CREATE TABLE sintomas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

CREATE TABLE pesos_sintomas (
    sintoma_id INT,
    sexo ENUM('M', 'F') NOT NULL,
    peso DECIMAL(4,3) NOT NULL,
    PRIMARY KEY (sintoma_id, sexo),
    FOREIGN KEY (sintoma_id) REFERENCES sintomas(id)
);

CREATE TABLE triagens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    medico_id INT NOT NULL,
    data_triagem TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    score_final DECIMAL(5,4), 
    recomendacao_teste TINYINT(1),
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    FOREIGN KEY (medico_id) REFERENCES medicos(id)
);

CREATE TABLE triagem_sintomas (
    triagem_id INT NOT NULL,
    sintoma_id INT NOT NULL,
    PRIMARY KEY (triagem_id, sintoma_id),
    FOREIGN KEY (triagem_id) REFERENCES triagens(id) ON DELETE CASCADE,
    FOREIGN KEY (sintoma_id) REFERENCES sintomas(id)
);