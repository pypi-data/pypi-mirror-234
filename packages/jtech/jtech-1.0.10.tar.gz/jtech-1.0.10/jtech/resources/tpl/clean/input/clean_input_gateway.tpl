/*
*  @(#){{ className }}InputGateway.java
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
package {{ package }}.application.ports.input;

import {{ package }}.application.core.domains.{{ className }};

/**
* class {{ className  }}InputGateway 
* 
* user {{ username  }} 
*/
public interface Create{{ className }}InputGateway {
    {{ className }} create({{ className }} {{ project }});
}
