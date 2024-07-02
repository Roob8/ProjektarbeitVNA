function plot_smith_chart_s1p(s1p_filename)
    % Check if the input file exists
    if ~isfile(s1p_filename)
        error('The specified S1P file does not exist.');
    end

    % Open the S1P file for reading
    fid = fopen(s1p_filename, 'r');
    if fid == -1
        error('Failed to open the S1P file.');
    end

    % Read the header of the S1P file
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
    if length(tokens) < 6
        error('Invalid S1P header format.');
    end
    freq_unit = tokens{2};
    data_format = tokens{4};

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
        if length(values) ~= 3
            error('Invalid S1P data format.');
        end
        data(end+1, :) = values; %#ok<*AGROW>
    end

    % Close the S1P file
    fclose(fid);

    % Extract relevant data
    freq = data(:, 1);
    if strcmpi(data_format, 'DB')
        s11_db = data(:, 2);
        s11_angle = data(:, 3);
        s11 = db_angle_to_complex(s11_db, s11_angle);
    elseif strcmpi(data_format, 'MA')
        s11_mag = data(:, 2);
        s11_angle = data(:, 3);
        s11 = mag_angle_to_complex(s11_mag, s11_angle);
    elseif strcmpi(data_format, 'RI')
        s11_real = data(:, 2);
        s11_imag = data(:, 3);
        s11 = s11_real + 1i * s11_imag;
    else
        error('Unsupported data format: %s', data_format);
    end

    % Plot the Smith chart
    figure;
    smithchart(s11);
    title('Smith Chart of S11 Parameters');
    xlabel('Real');
    ylabel('Imaginary');

    fprintf('Smith chart plotted for %s\n', s1p_filename);
end

function cplx = db_angle_to_complex(db, angle)
    % Convert dB to magnitude
    mag = 10.^(db/20);
    % Convert angle to radians
    angle_rad = deg2rad(angle);
    % Convert magnitude and angle to complex number
    cplx = mag .* exp(1i * angle_rad);
end

function cplx = mag_angle_to_complex(mag, angle)
    % Convert angle to radians
    angle_rad = deg2rad(angle);
    % Convert magnitude and angle to complex number
    cplx = mag .* exp(1i * angle_rad);
end
