/*
 *  @(#)KafkaConfiguration.java
 *
 *  Copyright (c) J-Tech Solucoes em Informatica.
 *  All Rights Reserved.
 *
 *  This software is the confidential and proprietary information of J-Tech.
 *  ("Confidential Information"). You shall not disclose such Confidential
 *  Information and shall use it only in accordance with the terms of the
 *  license agreement you entered into with J-Tech.
 *
 */
package {{ package }}.config.infra.kafka;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.kafka.support.converter.RecordMessageConverter;
import org.springframework.kafka.support.converter.StringJsonMessageConverter;

/**
 * Configuration for converter message kafka.
 *
 * class KafkaConfiguration
 * @author {{ username }}
 *
 */
@EnableKafka
@Configuration
public class KafkaConfiguration {

    /**
     * JsonConverter for Kafka messages.
     *
     * @return RecordMessageConvert json.
     */
    @Bean
    public RecordMessageConverter jsonConverter() {
        return new StringJsonMessageConverter();
    }
}
