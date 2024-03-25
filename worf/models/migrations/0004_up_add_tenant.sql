UPDATE worf_version SET version = 4;

CREATE TABLE tenant (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    data json,
    domain character varying(256),
    name character varying(60),
    email character varying,
    account_verified boolean DEFAULT false NOT NULL,
    new_email character varying,
    email_change_code character varying,
    disabled boolean DEFAULT false NOT NULL
);


CREATE SEQUENCE tenant_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY "tenant"
    ADD CONSTRAINT tenant_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY "tenant"
    ADD CONSTRAINT tenant_pkey PRIMARY KEY (id);

CREATE INDEX ix_tenant_account_verified ON "tenant" USING btree (account_verified);

CREATE INDEX ix_tenant_disabled ON "tenant" USING btree (disabled);

CREATE UNIQUE INDEX ix_tenant_domain ON "tenant" USING btree (domain);

CREATE UNIQUE INDEX ix_tenant_name ON "tenant" USING btree (name);

CREATE UNIQUE INDEX ix_tenant_email ON "tenant" USING btree (email);

CREATE INDEX ix_tenant_email_change_code ON "tenant" USING btree (email_change_code);

CREATE INDEX ix_tenant_new_email ON "tenant" USING btree (new_email);

ALTER SEQUENCE tenant_id_seq OWNED BY "tenant".id;

ALTER TABLE ONLY "tenant" ALTER COLUMN id SET DEFAULT nextval('tenant_id_seq'::regclass);

-- we add a tenant ID to all users
ALTER TABLE ONLY "user" ADD COLUMN tenant_id bigint;

-- we link the tenant ID to the tenant table
ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES tenant(id);

-- we add a tenant ID to all signup requests
ALTER TABLE ONLY signup_request ADD COLUMN tenant_id bigint;

-- we link the tenant ID to the tenant table
ALTER TABLE ONLY signup_request
    ADD CONSTRAINT signup_request_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES tenant(id);

-- invitation e-mails don't need to be unique anymore
DROP INDEX ix_invitation_email;
CREATE INDEX ix_invitation_email ON invitation USING btree (email);

-- signup requests should be unique on a per tenant basis
DROP INDEX ix_signup_request_email;
CREATE UNIQUE INDEX ix_signup_request_email_hash ON signup_request USING btree (email_hash, tenant_id);

-- we drop uniqueness on display name altogether
DROP INDEX ix_user_display_name;

-- emails need to be unique on a per tenant basis
DROP INDEX ix_user_email;
CREATE UNIQUE INDEX ix_user_email ON "user" USING btree (email, tenant_id);
