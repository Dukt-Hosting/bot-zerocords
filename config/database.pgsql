CREATE TABLE IF NOT EXISTS guild_settings(
    guild_id BIGINT PRIMARY KEY,
    prefix VARCHAR(30),
    worldnews_channel BIGINT,
    spacenews_channel BIGINT,
    audit_channel BIGINT,

    guild_moderator_role_id BIGINT, -- The guild moderator role
    muted_role_id BIGINT, -- The role muted members get

    kick_modlog_channel_id BIGINT,  -- The channel ID for mod actions to be posted to
    ban_modlog_channel_id BIGINT,
    mute_modlog_channel_id BIGINT,
    warn_modlog_channel_id BIGINT,

    edited_message_modlog_channel_id BIGINT,
    deleted_message_modlog_channel_id BIGINT,
    voice_update_modlog_channel_id BIGINT
);


CREATE TABLE IF NOT EXISTS user_settings(
    user_id BIGINT PRIMARY KEY
);


CREATE TABLE IF NOT EXISTS role_list(
    guild_id BIGINT,
    role_id BIGINT,
    key VARCHAR(50),
    value VARCHAR(50),
    PRIMARY KEY (guild_id, role_id, key)
);


CREATE TABLE IF NOT EXISTS channel_templates(
    guild_id BIGINT,
    template_data VARCHAR(2500)
);


CREATE TABLE IF NOT EXISTS channel_list(
    guild_id BIGINT,
    channel_id BIGINT,
    key VARCHAR(50),
    value VARCHAR(50),
    PRIMARY KEY (guild_id, channel_id, key)
);

DO $$ BEGIN
    CREATE TYPE moderation_action AS ENUM ('Mute', 'Warn', 'Kick', 'Ban', 'Unmute', 'Verify', 'Tempmute', 'Unban');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

CREATE TABLE IF NOT EXISTS infractions(
    infraction_id VARCHAR(10) PRIMARY KEY,
    guild_id BIGINT,
    moderator_id BIGINT,
    user_id BIGINT,
    infraction_type moderation_action,
    infraction_reason VARCHAR(60),
    timestamp TIMESTAMP,
    deleted_by BIGINT
);

CREATE TABLE IF NOT EXISTS temporary_roles(
    guild_id BIGINT,
    role_id BIGINT,
    user_id BIGINT,
    remove_timestamp TIMESTAMP,
    delete_role BOOLEAN NOT NULL DEFAULT FALSE,
    dm_user BOOLEAN NOT NULL DEFAULT TRUE,
    key VARCHAR(50),
    PRIMARY KEY (guild_id, role_id, user_id)
);

CREATE TABLE IF NOT EXISTS temporary_removed_roles(
    guild_id BIGINT,
    role_id BIGINT,
    user_id BIGINT,
    readd_timestamp TIMESTAMP,
    dm_user BOOLEAN NOT NULL DEFAULT TRUE,
    key VARCHAR(50),
    PRIMARY KEY (guild_id, role_id, user_id)
);