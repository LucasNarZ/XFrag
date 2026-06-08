INSERT INTO sintomas (id, nome) VALUES 
(1, 'Deficiência intelectual'),
(2, 'Face alongada/orelhas de abano'),
(3, 'Macroorquidismo'),
(4, 'Hipermobilidade articular'),
(5, 'Dificuldades de aprendizagem'),
(6, 'Déficit de atenção'),
(7, 'Movimentos repetitivos'),
(8, 'Atraso na fala'),
(9, 'Hiperatividade'),
(10, 'Evita contato visual'),
(11, 'Evita contato físico'),
(12, 'Agressividade');

-- masculinos
INSERT INTO pesos_sintomas (sintoma_id, sexo, peso) VALUES 
(1, 'M', 0.32), (2, 'M', 0.29), (3, 'M', 0.26), (4, 'M', 0.19), 
(5, 'M', 0.18), (6, 'M', 0.17), (7, 'M', 0.17), (8, 'M', 0.14), 
(9, 'M', 0.12), (10, 'M', 0.06), (11, 'M', 0.04), (12, 'M', 0.01);

-- femininos
INSERT INTO pesos_sintomas (sintoma_id, sexo, peso) VALUES 
(1, 'F', 0.20), (2, 'F', 0.09), (3, 'F', 0.00), (4, 'F', 0.04), 
(5, 'F', 0.28), (6, 'F', 0.12), (7, 'F', 0.05), (8, 'F', 0.01), 
(9, 'F', 0.04), (10, 'F', 0.08), (11, 'F', 0.07), (12, 'F', 0.02);