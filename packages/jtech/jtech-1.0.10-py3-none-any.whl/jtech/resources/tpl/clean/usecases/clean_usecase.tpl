/*
*  @(#){{ className  }}UseCase.java
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
package {{ package }}.application.core.usecases;


import {{ package }}.application.core.domains.{{ className }};
import {{ package }}.application.ports.input.Create{{ className }}InputGateway;
import {{ package }}.application.ports.output.Create{{ className }}OutputGateway;

/**
* class {{ className }}UseCase  
* 
* user {{ username }}  
*/
public class Create{{ className }}UseCase implements Create{{ className }}InputGateway {

    private final Create{{ className }}OutputGateway create{{ className }}OutputGateway;

    public Create{{ className }}UseCase(Create{{ className }}OutputGateway create{{ className }}OutputGateway) {
        this.create{{ className }}OutputGateway = create{{ className }}OutputGateway;
     }

    public {{ className }} create({{ className }} {{ project }}) {
        return create{{ className }}OutputGateway.create({{ project }});
     }
 }
