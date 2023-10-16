/*
*  @(#){{ className }}Entity.java
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
package {{ package }}.adapters.output.repositories.entities;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.util.UUID;

/**
* class {{ className  }}Entity 
* 
* user {{ username  }} 
*/
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class {{ className }}Entity implements Serializable {

    //@NotEmpty(message = "ID not generated")
    private UUID id;

    //Others parameters...

}
