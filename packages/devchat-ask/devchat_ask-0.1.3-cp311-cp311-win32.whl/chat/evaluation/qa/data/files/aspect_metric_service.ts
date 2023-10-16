import { getManager } from 'typeorm';
import { injectable } from 'inversify';
import { MartRepoAnalysisEmailAggregate } from '../../models/starrocks/data_center/mart_repo_analysis_email_aggregate';
import { Services } from '../../ioc/decorator';
import { Analyses } from '../../models/starrocks/ae/analyses';

@Services()
@injectable()
export class AspectMetricService {
  async queryAspectMetric(org_id: string, aspectTime?: Date, emails?: string[], repoIds?: string[], limit: number = 100, offset: number = 0): Promise<{ total: number; data: any[] }> {
    const em = getManager('starrocks');

    const qba = em.createQueryBuilder()
      .from(MartRepoAnalysisEmailAggregate, 'agg')
      .innerJoin(Analyses, 'ae', 'ae.analysis_id = agg.ae_analysis_id')
      .select('FIRST_VALUE(ae_analysis_id) OVER (PARTITION BY repo_id ORDER BY ae.start_time DESC)', 'analysis_id')
      .where('agg.org_id = :org_id', { org_id });
    if (repoIds !== undefined && repoIds.length > 0) {
      qba.andWhere('agg.repo_id IN (:...repoIds)', { repoIds });
    }
    if (aspectTime !== undefined) {
      qba.andWhere('ae.start_time <= :aspectTime', { aspectTime: Math.round(aspectTime.getTime() / 1000) });
    }
    const analysisIdsResult = await qba.getRawMany();
    const analysisIds = analysisIdsResult.map((item) => item.analysis_id);
    if (analysisIds.length === 0) {
      return { total: 0, data: [] };
    }
    const qb = em.createQueryBuilder()
      .from(MartRepoAnalysisEmailAggregate, 'agg')
      .innerJoin(Analyses, 'ae', 'ae.analysis_id = agg.ae_analysis_id')
      .select('agg.*')
      .addSelect('ae.start_time', 'analysis_time')
      .where('agg.org_id = :org_id', { org_id })
      .andWhere('agg.ae_analysis_id IN (:...analysisIds)', { analysisIds })
      .orderBy('agg.repo_id', 'ASC')
      .addOrderBy('agg.email', 'ASC');
    if (emails !== undefined && emails.length > 0) {
      qb.andWhere('agg.email IN (:...emails)', { emails });
    }
    const total = await qb.getCount();
    const data = await qb.limit(limit).offset(offset).getRawMany();

    return {
      total,
      data: data.map((item) => ({
        ...item,
        analysis_time: new Date(item.analysis_time * 1000),
      })),
    };
  }
}
