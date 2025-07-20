import { useState } from 'react';
import { DateRange } from 'react-date-range';
import { addDays } from 'date-fns';
import 'react-date-range/dist/styles.css';
import 'react-date-range/dist/theme/default.css';
import type { Range , RangeKeyDict} from 'react-date-range';

const DateRangePickerComponent = () => {
  const [range, setRange] = useState<Range[]>([
    {
      startDate: new Date(),
      endDate: addDays(new Date(), 7),
      key: 'selection'
    }
  ]);

  const handleSelect = (ranges: RangeKeyDict) => {
    setRange([ranges.selection]);
  };

  return (
    <div className="w-full max-w-full overflow-x-auto">
      <DateRange
        ranges={range}
        onChange={handleSelect}
        editableDateInputs={true}
        moveRangeOnFirstSelection={false}
      />
    </div>
  );
};

export default DateRangePickerComponent;
