/*
*  @(#){{ className }}UseCaseConfig.java
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
package {{ package }}.config.usecases;

import {{ package }}.adapters.output.Create{{ className }}Adapter;
import {{ package }}.application.core.usecases.Create{{ className }}UseCase;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
* class {{ className }}UseCaseConfig
* 
* user {{ username }}
*/
@Configuration
public class Create{{ className }}UseCaseConfig {

    @Bean
    public Create{{ className }}UseCase useCase(Create{{ className }}Adapter create{{ className }}Adapter) {
        return new Create{{ className }}UseCase(create{{ className }}Adapter);
     }

 }
