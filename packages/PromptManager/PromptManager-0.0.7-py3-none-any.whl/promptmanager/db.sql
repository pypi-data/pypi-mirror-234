CREATE TABLE class (
	id TEXT(50) NOT NULL primary key,
	name TEXT(255) NOT NULL,
	source TEXT(50) NOT NULL,
	role_prompt TEXT,
	type TEXT(50) NOT NULL,
	create_time INTEGER,
	update_time INTEGER,
	order_id INTEGER,
	user_id TEXT
);

CREATE TABLE prompt  (
	id TEXT(50) NOT NULL primary key,
	name TEXT(255) NOT NULL,
	note TEXT,
	prompt TEXT,
	source TEXT(50) NOT NULL,
	role_id TEXT(50),
	scene_id TEXT(50),
	labels_ids TEXT,
	variables TEXT,
	collecte_status TEXT(50),
	create_time INTEGER,
	update_time INTEGER,
	user_id TEXT
);

CREATE TABLE model  (
	id TEXT(50) NOT NULL primary key,
	name TEXT(255) NOT NULL,
	description TEXT,
	config TEXT NOT NULL,
	params TEXT NOT NULL,
	source TEXT(50) NOT NULL,
	enable_stream INTEGER,
	is_default INTEGER,
	create_time INTEGER,
	update_time INTEGER,
	user_id TEXT
);

CREATE TABLE module  (
	id TEXT(50) NOT NULL primary key,
	name TEXT(255) NOT NULL,
	description TEXT,
	source TEXT(50) NOT NULL,
	type TEXT(50) NOT NULL,
	"group" TEXT(50) NOT NULL,
	params TEXT NOT NULL,
	inputs TEXT NOT NULL,
	outputs TEXT NOT NULL,
	create_time INTEGER,
	update_time INTEGER,
	user_id TEXT
);

INSERT INTO module (id, name, description, "source", "type","group", params, inputs, outputs, create_time, update_time, user_id)
VALUES
('00000000-0000-0000-0000-000000000001', 'Input', 'Input', 'system', 'input','input', '[]', '[]', '[{"name":"assignment","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-0000-000000000002', 'Output', 'Output', 'system', 'output', 'output','[]', '[{"name":"result1","type":"any","defaultValue":null,"value":null}]', '[]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),

('00000000-0000-0000-aaaa-000000000001', 'Define Prompt', 'Define Prompt', 'system', 'prompt','prompt', '[]', '[]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-aaaa-000000000002', 'ChatMessagePromptTemplate', 'ChatMessagePromptTemplate', 'system', 'prompt','prompt', '[]', '[]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-aaaa-000000000003', 'ChatPromptTemplate', 'ChatPromptTemplate', 'system', 'prompt','prompt', '[]', '[]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-aaaa-000000000004', 'HumanMessagePromptTemplate', 'HumanMessagePromptTemplate', 'system', 'prompt','prompt', '[]', '[]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-aaaa-000000000005', 'PromptTemplate', 'PromptTemplate', 'system', 'prompt','prompt', '[]', '[]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-aaaa-000000000006', 'SystemMessagePromptTemplate', 'SystemMessagePromptTemplate', 'system', 'prompt','prompt', '[]', '[]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),

('00000000-0000-0000-1111-000000000001', 'Python3 Script', 'Python3 Script', 'system','script', 'tool', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"true"}]', '[{"name":"input","type":"any","defaultValue":"","value":null,"description":""}]', '[{"name":"output","type":"any","defaultValue":"","value":null,"description":""}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-bbbb-000000000001', 'Text segmentation', 'Text segmentation', 'system','script', 'tool', '[{"name":"script","type":"script","default_value":"","value":"","editable":"false"},{"name":"chunk_size","type":"int","default_value":"","value":""},{"name":"chunk_overlap","type":"int","default_value":"","value":""},{"name":"separators","type":"text","default_value":"","value":""}]', '[{"name":"input","type":"any","defaultValue":"","value":null,"description":""}]', '[{"name":"output","type":"any","defaultValue":"","value":null,"description":""}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-bbbb-000000000002', 'Text truncation', 'Text truncation', 'system','script', 'tool', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"max_length","type":"int","default_value":"","value":""}]', '[{"name":"input","type":"any","defaultValue":"","value":null,"description":""}]', '[{"name":"output","type":"any","defaultValue":"","value":null,"description":""}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-bbbb-000000000003', 'Character TextSpliter', 'Character TextSpliter', 'system','script', 'tool', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"true"}]', '[{"name":"input","type":"any","defaultValue":"","value":null,"description":""}]', '[{"name":"output","type":"any","defaultValue":"","value":null,"description":""}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-bbbb-000000000004', 'Recursive Character Text', 'Recursive Character Text', 'system','script', 'tool', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"true"}]', '[{"name":"input","type":"any","defaultValue":"","value":null,"description":""}]', '[{"name":"output","type":"any","defaultValue":"","value":null,"description":""}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),

('00000000-0000-0000-cccc-000000000002', 'Chroma Reader', 'Chroma Reader', 'system', 'vectordb','vectordb', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"Host","type":"text","options":[],"default_value":"","value":""},{"name":"Port","type":"text","options":[],"default_value":"","value":""},{"name":"Connection","type":"text","options":[],"default_value":"","value":""},{"name":"n_results","type":"int","options":[],"default_value":"10","value":""}]', '[{"name":"input","type":"any","defaultValue":null,"value":null}]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-cccc-000000000003', 'FAISS Reader', 'FAISS Reader', 'system', 'vectordb','vectordb', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"Host","type":"text","options":[],"default_value":"","value":""},{"name":"Port","type":"text","options":[],"default_value":"","value":""},{"name":"Connection","type":"text","options":[],"default_value":"","value":""}]', '[{"name":"input","type":"any","defaultValue":null,"value":null}]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-cccc-000000000004', 'DingoDB Reader', 'DingoDB Reader', 'system', 'vectordb','vectordb', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"Host","type":"text","options":[],"default_value":"","value":""},{"name":"Port","type":"text","options":[],"default_value":"","value":""},{"name":"Index","type":"text","options":[],"default_value":"","value":""},{"name":"user","type":"text","options":[],"default_value":"","value":""},{"name":"password","type":"text","options":[],"default_value":"","value":""}]', '[{"name":"input","type":"any","defaultValue":null,"value":null}]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-cccc-000000000005', 'Chroma Writer', 'Chroma Writer', 'system', 'vectordb','vectordb', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"Host","type":"text","options":[],"default_value":"","value":""},{"name":"Port","type":"text","options":[],"default_value":"","value":""},{"name":"Connection","type":"text","options":[],"default_value":"","value":""},{"name":"n_results","type":"int","options":[],"default_value":"10","value":""}]', '[{"name":"input","type":"any","defaultValue":null,"value":null}]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-cccc-000000000006', 'FAISS Writer', 'FAISS Writer', 'system', 'vectordb','vectordb', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"Host","type":"text","options":[],"default_value":"","value":""},{"name":"Port","type":"text","options":[],"default_value":"","value":""},{"name":"Connection","type":"text","options":[],"default_value":"","value":""}]', '[{"name":"input","type":"any","defaultValue":null,"value":null}]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-cccc-000000000007', 'DingoDB Writer', 'DingoDB Writer', 'system', 'vectordb','vectordb', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"Host","type":"text","options":[],"default_value":"","value":""},{"name":"Port","type":"text","options":[],"default_value":"","value":""},{"name":"Index","type":"text","options":[],"default_value":"","value":""},{"name":"user","type":"text","options":[],"default_value":"","value":""},{"name":"password","type":"text","options":[],"default_value":"","value":""}]', '[{"name":"input","type":"any","defaultValue":null,"value":null}]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-cccc-000000000008', 'MultiQueryRetriever', 'MultiQueryRetriever', 'system', 'vectordb','vectordb', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"Host","type":"text","options":[],"default_value":"","value":""},{"name":"Port","type":"text","options":[],"default_value":"","value":""},{"name":"Index","type":"text","options":[],"default_value":"","value":""},{"name":"user","type":"text","options":[],"default_value":"","value":""},{"name":"password","type":"text","options":[],"default_value":"","value":""}]', '[{"name":"input","type":"any","defaultValue":null,"value":null}]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),

('00000000-0000-0000-dddd-000000000001', 'AgentIntitalzer', 'AgentIntitalzer', 'system', 'agent','agent', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"Host","type":"text","options":[],"default_value":"","value":""},{"name":"Port","type":"text","options":[],"default_value":"","value":""},{"name":"Connection","type":"text","options":[],"default_value":"","value":""},{"name":"n_results","type":"int","options":[],"default_value":"10","value":""}]', '[{"name":"input","type":"any","defaultValue":null,"value":null}]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-dddd-000000000002', 'CSVAgent', 'CSVAgent', 'system', 'agent','agent', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"Host","type":"text","options":[],"default_value":"","value":""},{"name":"Port","type":"text","options":[],"default_value":"","value":""},{"name":"Connection","type":"text","options":[],"default_value":"","value":""}]', '[{"name":"input","type":"any","defaultValue":null,"value":null}]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-dddd-000000000003', 'JsonAgent', 'JsonAgent', 'system', 'agent','agent', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"Host","type":"text","options":[],"default_value":"","value":""},{"name":"Port","type":"text","options":[],"default_value":"","value":""},{"name":"Index","type":"text","options":[],"default_value":"","value":""},{"name":"user","type":"text","options":[],"default_value":"","value":""},{"name":"password","type":"text","options":[],"default_value":"","value":""}]', '[{"name":"input","type":"any","defaultValue":null,"value":null}]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-dddd-000000000004', 'OpenAI Conversationl', 'OpenAI Conversationl', 'system', 'agent','agent', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"Host","type":"text","options":[],"default_value":"","value":""},{"name":"Port","type":"text","options":[],"default_value":"","value":""},{"name":"Index","type":"text","options":[],"default_value":"","value":""},{"name":"user","type":"text","options":[],"default_value":"","value":""},{"name":"password","type":"text","options":[],"default_value":"","value":""}]', '[{"name":"input","type":"any","defaultValue":null,"value":null}]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-dddd-000000000005', 'VectorStoreAgent', 'VectorStoreAgent', 'system', 'agent','agent', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"Host","type":"text","options":[],"default_value":"","value":""},{"name":"Port","type":"text","options":[],"default_value":"","value":""},{"name":"Index","type":"text","options":[],"default_value":"","value":""},{"name":"user","type":"text","options":[],"default_value":"","value":""},{"name":"password","type":"text","options":[],"default_value":"","value":""}]', '[{"name":"input","type":"any","defaultValue":null,"value":null}]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-dddd-000000000006', 'ZeroShotAgent', 'ZeroShotAgent', 'system', 'agent','agent', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"Host","type":"text","options":[],"default_value":"","value":""},{"name":"Port","type":"text","options":[],"default_value":"","value":""},{"name":"Index","type":"text","options":[],"default_value":"","value":""},{"name":"user","type":"text","options":[],"default_value":"","value":""},{"name":"password","type":"text","options":[],"default_value":"","value":""}]', '[{"name":"input","type":"any","defaultValue":null,"value":null}]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),

('00000000-0000-0000-eeee-000000000001', 'CSVLoader', 'CSVLoader', 'system', 'loader','loader', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"Host","type":"text","options":[],"default_value":"","value":""},{"name":"Port","type":"text","options":[],"default_value":"","value":""},{"name":"Connection","type":"text","options":[],"default_value":"","value":""},{"name":"n_results","type":"int","options":[],"default_value":"10","value":""}]', '[{"name":"input","type":"any","defaultValue":null,"value":null}]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-eeee-000000000002', 'TextLoader', 'TextLoader', 'system', 'loader','loader', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"Host","type":"text","options":[],"default_value":"","value":""},{"name":"Port","type":"text","options":[],"default_value":"","value":""},{"name":"Connection","type":"text","options":[],"default_value":"","value":""}]', '[{"name":"input","type":"any","defaultValue":null,"value":null}]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),

('00000000-0000-0000-ffff-000000000001', 'CohereEmbeddings', 'CohereEmbeddings', 'system', 'embedding','embedding', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"Host","type":"text","options":[],"default_value":"","value":""},{"name":"Port","type":"text","options":[],"default_value":"","value":""},{"name":"Connection","type":"text","options":[],"default_value":"","value":""},{"name":"n_results","type":"int","options":[],"default_value":"10","value":""}]', '[{"name":"input","type":"any","defaultValue":null,"value":null}]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-ffff-000000000002', 'HuggingFaceEmbeddings', 'HuggingFaceEmbeddings', 'system', 'embedding','embedding', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"Host","type":"text","options":[],"default_value":"","value":""},{"name":"Port","type":"text","options":[],"default_value":"","value":""},{"name":"Connection","type":"text","options":[],"default_value":"","value":""}]', '[{"name":"input","type":"any","defaultValue":null,"value":null}]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),
('00000000-0000-0000-ffff-000000000003', 'OpenAIEmbeddings', 'OpenAIEmbeddings', 'system', 'embedding','embedding', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"Host","type":"text","options":[],"default_value":"","value":""},{"name":"Port","type":"text","options":[],"default_value":"","value":""},{"name":"Connection","type":"text","options":[],"default_value":"","value":""},{"name":"n_results","type":"int","options":[],"default_value":"10","value":""}]', '[{"name":"input","type":"any","defaultValue":null,"value":null}]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001'),

('00000000-0000-0000-1111-000000000002', 'Prompt Runner', 'Prompt Runner', 'system', 'chains','chains', '[{"name":"script","type":"script","options":[],"default_value":"","value":"","editable":"false"},{"name":"Host","type":"text","options":[],"default_value":"","value":""},{"name":"Port","type":"text","options":[],"default_value":"","value":""},{"name":"Connection","type":"text","options":[],"default_value":"","value":""},{"name":"n_results","type":"int","options":[],"default_value":"10","value":""}]', '[{"name":"input","type":"any","defaultValue":null,"value":null}]', '[{"name":"output","type":"any","defaultValue":null,"value":null}]', 1691978400, 1691978400, '00000000-1111-0000-000a-000000000001');


CREATE TABLE flow  (
	id TEXT(50) NOT NULL primary key,
	name TEXT(255) NOT NULL,
	description TEXT,
	config TEXT NOT NULL,
	model_ids TEXT,
	params TEXT NOT NULL,
	source TEXT(50) NOT NULL,
	prompt_count INTEGER,
	create_time INTEGER,
	update_time INTEGER,
	user_id TEXT
);

CREATE TABLE app  (
	id TEXT(50) NOT NULL primary key,
	name TEXT(255) NOT NULL,
	description TEXT,
	flow_id id TEXT(50),
	input_info TEXT,
	source TEXT(50) NOT NULL,
	create_time INTEGER,
	update_time INTEGER,
	user_id TEXT
);

INSERT INTO class
(id, name, "source", role_prompt, "type", create_time, update_time, order_id, user_id)
VALUES('00000000-0000-0000-0000-000000000001', 'Others', 'system', 'Preset Scene ','scene', 1691978400,1691978400, 2147483647, '00000000-1111-0000-000a-000000000001');
INSERT INTO class
(id, name, "source", role_prompt, "type", create_time, update_time, order_id, user_id)
VALUES('00000000-0000-0000-0000-000000000002', 'None', 'system', 'Preset Role ','role', 1691978400,1691978400, 1, '00000000-1111-0000-000a-000000000001');
