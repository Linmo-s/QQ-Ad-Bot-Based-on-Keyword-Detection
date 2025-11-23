package com.qqbot.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.qqbot.model.BotConfig;
import org.springframework.stereotype.Service;

import java.io.File;

@Service
public class ConfigService {

    private final String configPath = "src/main/java/com/qqbot/resources/config.json";
    private final ObjectMapper mapper = new ObjectMapper();

    /** 读取配置 */
    public BotConfig loadConfig() throws Exception {
        return mapper.readValue(new File(configPath), BotConfig.class);
    }

    /** 保存配置 */
    public void saveConfig(BotConfig config) throws Exception {
        mapper.writerWithDefaultPrettyPrinter()
              .writeValue(new File(configPath), config);
    }
}
