function convert_s2p_to_excel(s2p_filename, excel_filename)
    % Check if the input file exists
    if ~isfile(s2p_filename)
        error('The specified S2P file does not exist.');
    end

    % Open the S2P file for reading
    fid = fopen(s2p_filename, 'r');
    if fid == -1
        error('Failed to open the S2P file.');
    end

    % Read the header of the S2P file
    header = {};
    while true
        line = fgetl(fid);
        if ~ischar(line)
            error('Unexpected end of file.');
        end
        header{end+1} = line; %#ok<*AGROW>
        if startsWith(line, '#')
            break;
        end
    end

    % Determine the format and frequency unit
    header_line = header{end};
    tokens = strsplit(header_line);
    if length(tokens) < 7
        error('Invalid S2P header format.');
    end
    freq_unit = tokens{2};
    data_format = tokens{4};
    if ~strcmpi(data_format, 'DB')
        error('This script only supports S-parameters in dB format.');
    end

    % Read the S-parameter data
    data = [];
    while true
        line = fgetl(fid);
        if ~ischar(line)
            break;
        end
        if isempty(line) || startsWith(line, '!')
            continue;
        end
        values = str2double(strsplit(line));
        values = values(2:end-1);
        if length(values) ~= 9
            error('Invalid S2P data format.');
        end
        data(end+1, :) = values; %#ok<*AGROW>
    end

    % Close the S2P file
    fclose(fid);

    % Extract relevant data
    freq = data(:, 1);
    s11_db = data(:, 2);
    s11_angle = data(:, 3);
    s21_db = data(:, 4);
    s21_angle = data(:, 5);
    s12_db = data(:, 6);
    s12_angle = data(:, 7);
    s22_db = data(:, 8);
    s22_angle = data(:, 9);

    % Convert dB and angle to real and imaginary parts
    s11 = db_angle_to_complex(s11_db, s11_angle);
    s21 = db_angle_to_complex(s21_db, s21_angle);
    s12 = db_angle_to_complex(s12_db, s12_angle);
    s22 = db_angle_to_complex(s22_db, s22_angle);

    % Create a table with the data
    T = table(freq, real(s11), imag(s11), real(s21), imag(s21), real(s12), imag(s12), real(s22), imag(s22), ...
        'VariableNames', {'Frequency', 'S11_Real', 'S11_Imag', 'S21_Real', 'S21_Imag', 'S12_Real', 'S12_Imag', 'S22_Real', 'S22_Imag'});

    % Write the table to an Excel file
    writetable(T, excel_filename);

    fprintf('Conversion completed: %s -> %s\n', s2p_filename, excel_filename);
end

function cplx = db_angle_to_complex(db, angle)
    % Convert dB to magnitude
    mag = 10.^(db/20);
    % Convert angle to radians
    angle_rad = deg2rad(angle);
    % Convert magnitude and angle to complex number
    cplx = mag .* exp(1i * angle_rad);
end
