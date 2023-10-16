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
import org.springframework.beans.BeanUtils;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.TypeAlias;
import org.springframework.data.mongodb.core.mapping.Document;

import java.io.Serializable;
import java.util.Objects;

/**
* class {{ className  }}Entity 
* 
* @author {{ username  }}
*/
@Data
@Builder
@Document("{{ project }}s")
@AllArgsConstructor
@NoArgsConstructor
@TypeAlias("{{ className }}")
@ToString
public class {{ className }}Entity implements Serializable {

    @Id
    private String id;

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
