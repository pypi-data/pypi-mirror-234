/*
*  @(#){{ className }}Adapter.java
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
package {{ package }}.adapters.output;

import {{ package }}.application.core.domains.{{ className }};
import {{ package }}.application.ports.output.Create{{ className }}OutputGateway;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

/**
* class {{ className }}Adapter 
* 
* user {{ username }}  
*/
@Component
@RequiredArgsConstructor
public class Create{{ className }}Adapter implements Create{{ className }}OutputGateway {

    // private final {{ className }}Repository repository;

    @Override
    public {{ className }} create({{ className }} {{ project }}) {
       // return this.repository.save({{ project }});
          return {{ project }};
    }

}