package com.qqbot.model;

import lombok.Data;

@Data
public class GlobalConfig {
    private int triggerCount;
    private String keywords;
    private String textMessage;
    private String imagePath;
}
