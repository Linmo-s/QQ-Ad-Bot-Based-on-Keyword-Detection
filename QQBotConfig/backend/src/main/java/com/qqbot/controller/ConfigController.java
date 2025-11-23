package com.qqbot.controller;

import com.qqbot.model.BotConfig;
import com.qqbot.service.ConfigService;
import org.springframework.web.bind.annotation.*;

@CrossOrigin
@RestController
@RequestMapping("/api/config")
public class ConfigController {

    private final ConfigService configService;

    public ConfigController(ConfigService configService) {
        this.configService = configService;
    }

    /** 获取配置 */
    @GetMapping
    public BotConfig getConfig() throws Exception {
        return configService.loadConfig();
    }

    /** 更新配置 */
    @PostMapping
    public String updateConfig(@RequestBody BotConfig config) throws Exception {
        configService.saveConfig(config);
        return "OK";
    }
}
