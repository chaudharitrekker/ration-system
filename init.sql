--
-- PostgreSQL database dump
--

\restrict H1kcMwPNPIKUJQiG6aSz6ceTK3v4N66bCEsqRiEbfA7eWQwNuWBLJeNeLA9h6xY

-- Dumped from database version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: rationuser
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO rationuser;

--
-- Name: demand; Type: TABLE; Schema: public; Owner: rationuser
--

CREATE TABLE public.demand (
    id integer NOT NULL,
    requested_sugar integer NOT NULL,
    requested_oil integer NOT NULL,
    approved_sugar integer,
    approved_oil integer,
    status character varying(20),
    date_created timestamp without time zone,
    employee_code character varying(50) NOT NULL
);


ALTER TABLE public.demand OWNER TO rationuser;

--
-- Name: demand_id_seq; Type: SEQUENCE; Schema: public; Owner: rationuser
--

CREATE SEQUENCE public.demand_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.demand_id_seq OWNER TO rationuser;

--
-- Name: demand_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rationuser
--

ALTER SEQUENCE public.demand_id_seq OWNED BY public.demand.id;


--
-- Name: officer_demands; Type: TABLE; Schema: public; Owner: rationuser
--

CREATE TABLE public.officer_demands (
    id integer NOT NULL,
    employee_number character varying(50) NOT NULL,
    name character varying(100) NOT NULL,
    rank character varying(50) NOT NULL,
    ration_type character varying(10) NOT NULL,
    address text NOT NULL,
    unit character varying(100) NOT NULL,
    office_phone character varying(10) NOT NULL,
    mobile character varying(15) NOT NULL,
    collection_type character varying(50) NOT NULL,
    bank_account character varying(30) NOT NULL,
    ifsc character varying(20) NOT NULL,
    rik_gx_number character varying(50) NOT NULL,
    rik_gx_date date NOT NULL,
    rik_gx_file character varying(200),
    retirement_date date,
    promotion_gx_number character varying(50),
    promotion_gx_date date,
    date_created timestamp without time zone,
    status character varying(20),
    availability_days integer,
    created_by character varying(20)
);


ALTER TABLE public.officer_demands OWNER TO rationuser;

--
-- Name: officer_demands_id_seq; Type: SEQUENCE; Schema: public; Owner: rationuser
--

CREATE SEQUENCE public.officer_demands_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.officer_demands_id_seq OWNER TO rationuser;

--
-- Name: officer_demands_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rationuser
--

ALTER SEQUENCE public.officer_demands_id_seq OWNED BY public.officer_demands.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: rationuser
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password_hash character varying(256) NOT NULL,
    role character varying(20) NOT NULL
);


ALTER TABLE public.users OWNER TO rationuser;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: rationuser
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO rationuser;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rationuser
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: demand id; Type: DEFAULT; Schema: public; Owner: rationuser
--

ALTER TABLE ONLY public.demand ALTER COLUMN id SET DEFAULT nextval('public.demand_id_seq'::regclass);


--
-- Name: officer_demands id; Type: DEFAULT; Schema: public; Owner: rationuser
--

ALTER TABLE ONLY public.officer_demands ALTER COLUMN id SET DEFAULT nextval('public.officer_demands_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: rationuser
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: rationuser
--

COPY public.alembic_version (version_num) FROM stdin;
e1363bbbf1ba
\.


--
-- Data for Name: demand; Type: TABLE DATA; Schema: public; Owner: rationuser
--

COPY public.demand (id, requested_sugar, requested_oil, approved_sugar, approved_oil, status, date_created, employee_code) FROM stdin;
1	2	1	1	2	Delivered	2025-09-04 10:53:29.636192	22222
2	2	2	2	0	Delivered	2025-09-08 05:57:38.059862	22222
3	1	1	3	-1	Delivered	2025-09-08 06:26:28.65938	22222
\.


--
-- Data for Name: officer_demands; Type: TABLE DATA; Schema: public; Owner: rationuser
--

COPY public.officer_demands (id, employee_number, name, rank, ration_type, address, unit, office_phone, mobile, collection_type, bank_account, ifsc, rik_gx_number, rik_gx_date, rik_gx_file, retirement_date, promotion_gx_number, promotion_gx_date, date_created, status, availability_days, created_by) FROM stdin;
1	22222	Officer Name	Rank	EV	mumbai	Unit B	12345	1234567890	DELIVERY	987654321Abc	sdgv1234	1234asdf	2025-09-11	dd12-13_0.pdf	2025-09-12	asdfjkl;123	2025-09-22	2025-09-10 09:58:34.15746	\N	\N	\N
2	11111	Officer Name	Rank	PV	R123	Unit A	21345	2134432112	SELF	1234567890	qwer1234	qwer1234	2025-01-01	dd12-13_0.pdf	2025-02-02	qwer1243	2025-03-03	2025-09-10 11:11:26.478068	\N	\N	\N
46	12345	Rajesh Singh	5	PV	test	Unit A	test	test	SELF	test	test	test	2025-09-19	dd12-13_0.pdf	2025-09-20	test	2025-09-27	2025-09-18 10:35:06.575294	Pending	\N	12345
6	22222	Unknown Officer	Unknown Rank	PV	mambai	Unit A	12341	12341234	SELF	12341243	12431243	12431243	2025-09-10	dd12-13_0.pdf	2025-09-13	12431243	2025-09-19	2025-09-12 09:09:48.993358	Approved	7	22222
13	12345	Rajesh Singh	5	PV	qwer	Unit A	qwer	qwer	SELF	qwer	wqer	wqr	2025-09-15	dd12-13_0.pdf	2025-09-16	wqer	2025-09-17	2025-09-15 09:04:22.684355	Approved	4	12345
9	54321	Unknown Officer	Unknown Rank	PV	asdf	Unit A	asdf	asdf	SELF	asdf	sadf	sadf	2025-09-10	dd12-13_0.pdf	2025-09-10	asdf	2025-09-13	2025-09-12 11:35:13.196599	Approved	7	54321
25	22222	Anil Gupta	6	PV	qwer	Unit A	qwerr	qwer	SELF	qwerqw	qwerqwer	qwerqwer	2025-09-18	dd12-13_0.pdf	2025-09-18	qwerqwer	2025-09-25	2025-09-17 05:24:49.086492	Pending	\N	22222
26	54321	Ajay Kumar	3	PV	qwer	Unit A	qwerr	qwerr	SELF	qwer	qwer	wqer	2025-09-18	dd12-13_0.pdf	2025-09-19	wqer	2025-09-20	2025-09-17 05:41:59.827327	Pending	\N	54321
27	22222	Anil Gupta	6	EV	qwerqwer	Unit A	qwerw	qqwerwqer	SELF	qwerr	qwerwq	wqer	2025-09-18	dd12-13_0.pdf	2025-09-25	qwerr	2025-09-19	2025-09-17 05:51:50.168616	Approved	2	22222
28	54321	Ajay Kumar	3	PV	asdfa	Unit A	sadf	sdfs	SELF	sadfasd	fasdf	sadfasdf	2025-09-19	dd12-13_0.pdf	2025-09-19	sadfsadf	2025-09-20	2025-09-18 04:49:10.984113	Pending	\N	54321
29	12344	Rajesh Bhaker	POEL_R	PV	mumbai 4	Unit C	12434	1234124343	SELF	1243	1243	1243	2025-09-19	dd12-13_0.pdf	2025-10-09	12434	2025-09-10	2025-09-18 05:45:00.319806	Approved	\N	raiser
30	wqer	qwer	wqer	PV	qwer	Unit A	wqer	qwer	SELF	qwer	wqer	wqer	2025-09-19	\N	2025-09-19	qwer	2025-09-19	2025-09-18 06:54:02.583731	Pending	\N	raiser
31	12345	Rajesh Singh	5	EV	qwer	Unit A	qwer	wqer	SELF	wqer	qwer	wqer	2025-09-17	dd12-13_0.pdf	2025-09-22	qwerqw	2025-09-19	2025-09-18 06:57:50.106089	Pending	\N	12345
32	12345	Rajesh Singh	5	EV	qwer	Unit A	qwer	wqer	SELF	wqer	qwer	wqer	2025-09-17	dd12-13_0.pdf	2025-09-22	qwerqw	2025-09-19	2025-09-18 06:58:00.157476	Pending	\N	12345
33	12345	Rajesh Singh	5	EV	qwer	Unit A	qwer	wqer	SELF	wqer	qwer	wqer	2025-09-17	dd12-13_0.pdf	2025-09-22	qwerqw	2025-09-19	2025-09-18 06:58:05.907775	Pending	\N	12345
34	12345	Rajesh Singh	5	EV	qwer	Unit A	qwer	wqer	SELF	wqer	qwer	wqer	2025-09-17	dd12-13_0.pdf	2025-09-22	qwerqw	2025-09-19	2025-09-18 06:58:11.611318	Pending	\N	12345
35	12345	Rajesh Singh	5	EV	qwer	Unit A	qwer	wqer	SELF	wqer	qwer	wqer	2025-09-17	dd12-13_0.pdf	2025-09-22	qwerqw	2025-09-19	2025-09-18 06:58:18.460059	Pending	\N	12345
36	12345	Rajesh Singh	5	EV	qwer	Unit A	qwer	wqer	SELF	wqer	qwer	wqer	2025-09-17	dd12-13_0.pdf	2025-09-22	qwerqw	2025-09-19	2025-09-18 06:58:28.682664	Pending	\N	12345
37	12345	Rajesh Singh	5	EV	qwer	Unit A	qwer	wqer	SELF	wqer	qwer	wqer	2025-09-17	dd12-13_0.pdf	2025-09-22	qwerqw	2025-09-19	2025-09-18 06:58:31.942406	Pending	\N	12345
38	12345	Rajesh Singh	5	EV	qwer	Unit A	qwer	wqer	SELF	wqer	qwer	wqer	2025-09-17	dd12-13_0.pdf	2025-09-22	qwerqw	2025-09-19	2025-09-18 06:58:35.325419	Pending	\N	12345
39	12345	Rajesh Singh	5	EV	qwer	Unit A	qwer	wqer	SELF	wqer	qwer	wqer	2025-09-17	dd12-13_0.pdf	2025-09-22	qwerqw	2025-09-19	2025-09-18 06:59:00.732319	Pending	\N	12345
40	12345	Rajesh Singh	5	EV	qwer	Unit A	qwer	wqer	SELF	wqer	qwer	wqer	2025-09-17	dd12-13_0.pdf	2025-09-22	qwerqw	2025-09-19	2025-09-18 06:59:03.918295	Pending	\N	12345
41	12345	Rajesh Singh	5	EV	qwer	Unit A	qwer	wqer	SELF	wqer	qwer	wqer	2025-09-17	dd12-13_0.pdf	2025-09-22	qwerqw	2025-09-19	2025-09-18 06:59:06.994076	Pending	\N	12345
42	12345	Rajesh Singh	5	EV	qwer	Unit A	qwer	wqer	SELF	wqer	qwer	wqer	2025-09-17	dd12-13_0.pdf	2025-09-22	qwerqw	2025-09-19	2025-09-18 06:59:11.146301	Pending	\N	12345
43	22222	Anil Gupta	6	EV	mumbai	Unit C	12354	12345666	SELF	qwer12343	1243qwer	qwer1243	2025-09-19	dd12-13_0.pdf	2025-09-19	12432143	2025-09-19	2025-09-18 09:35:34.195607	Pending	\N	22222
18	1234	test	test	PV	1234	Unit A	12341	12341234	SELF	12431243	12431243	12431243	2025-09-18	dd12-13_0.pdf	2025-09-19	12431243	2025-09-19	2025-09-17 04:32:02.095931	Approved	\N	raiser
44	qwer	qwer	qwer	PV	q	Unit A	qwer	qwer	SELF	qwer	qwer	qwer	2025-09-19	\N	2025-09-25	qwer	2025-09-29	2025-09-18 10:26:54.874586	Pending	\N	raiser
45	12345	Rajesh Singh	5	PV	test	Unit A	test	test	SELF	test	test	test	2025-09-19	dd12-13_0.pdf	2025-09-20	test	2025-09-27	2025-09-18 10:34:51.947966	Pending	\N	12345
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: rationuser
--

COPY public.users (id, username, password_hash, role) FROM stdin;
3	raiser1	scrypt:32768:8:1$7REHT1x71hEpy7Rn$7225769a86e9ae715b961b6bf2980b7c4f1578c844e656aa47b050cd7e0165c2bfa994a299c37b4b9160161064ed220541fa5f45c36c08f9c50c884b3f43703a	raiser
4	issuer1	scrypt:32768:8:1$GwxWcyQLUWuDvtng$bfa5be7bd1cc1c0f32420993d726176b0adaf489d3676798a67e49d87671fbcfbdcfae47eb87ffb0f53ca22012b48c9039387c0d9259b395224503f735bea3ba	issuer
\.


--
-- Name: demand_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rationuser
--

SELECT pg_catalog.setval('public.demand_id_seq', 3, true);


--
-- Name: officer_demands_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rationuser
--

SELECT pg_catalog.setval('public.officer_demands_id_seq', 46, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rationuser
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: rationuser
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: demand demand_pkey; Type: CONSTRAINT; Schema: public; Owner: rationuser
--

ALTER TABLE ONLY public.demand
    ADD CONSTRAINT demand_pkey PRIMARY KEY (id);


--
-- Name: officer_demands officer_demands_pkey; Type: CONSTRAINT; Schema: public; Owner: rationuser
--

ALTER TABLE ONLY public.officer_demands
    ADD CONSTRAINT officer_demands_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: rationuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: rationuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- PostgreSQL database dump complete
--

\unrestrict H1kcMwPNPIKUJQiG6aSz6ceTK3v4N66bCEsqRiEbfA7eWQwNuWBLJeNeLA9h6xY

