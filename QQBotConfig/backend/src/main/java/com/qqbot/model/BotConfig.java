package com.qqbot.model;

import lombok.Data;
import java.util.List;

@Data
public class BotConfig {
    private GlobalConfig global_config;
    private List<TargetGroup> target_groups;
}
