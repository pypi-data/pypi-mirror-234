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
package {{ package }}.entities;


import lombok.*;

import java.io.Serializable;
import java.util.Objects;
import java.util.UUID;

/**
* class {{ className  }}Entity 
* 
* @author {{ username  }}
*/
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@ToString
public class {{ className }}Entity implements Serializable {

    //@Id
    private UUID id;

    //Others parameters...

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        {{ className }}Entity that = ({{ className }}Entity) o;
        return Objects.equals(id, that.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

}
